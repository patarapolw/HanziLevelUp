$(document).ready(function() {
  $.post('/post/hanzi/getAll', function(knownHanzi) {
    $.post('/post/file/getLevels', function(hanziLevelsRaw) {
      const hanziLevels = hanziLevelsRaw.trim().split('\n');
      let level = 0;
      for(let i=0; i<hanziLevels.length; i++){
        const element = $('<tr></tr>');
        if(hanziLevels[i].match(/\p{UIdeo}/u) !== null){
          level++;
          element.append('<td style="text-align: right;">{0}</td>'.format(level));
          const td = $('<td></td>');
          const hanziInLevel = hanziLevels[i].split("");
          for(let j=0; j<hanziInLevel.length; j++){
            let hanziClass;
            if(knownHanzi.indexOf(hanziInLevel[j]) !== -1){
              hanziClass = "knownHanzi";
            } else {
              hanziClass = "notKnownHanzi";
            }
            td.append('<div class="hanzi {1}">{0}</div>'.format(hanziInLevel[j], hanziClass));
          }
          element.append(td);
          element.addClass('entry');
        } else {
          element.append('<td style="padding-left: 50px;" colspan="2">{0}</td>'.format(hanziLevels[i]));
        }
        $('.hanziShowcase').append(element);
      }
    });
  });

  $.contextMenu({
    selector: ".entry",
    items: {
      learnNewHanzi: {
        name: "Learn new Hanzi",
        callback: function(key, opt){
          const allHanzi = getCurrentLevelHanzi('.notKnownHanzi', this);

          if(allHanzi === ""){
            alert('All Hanzi in this level are learnt.');
          } else {
            Cookies.set('allHanzi', allHanzi);
            window.location.href = "/learnHanzi";
          }
        }
      },
      reviewHanzi: {
        name: "Review Hanzi",
        callback: function(key, opt){
          const allHanzi = getCurrentLevelHanzi('.knownHanzi', this);

          if(allHanzi === ""){
            alert('Please learn new Hanzi first.');
          } else {
            Cookies.set('allHanzi', allHanzi);
            window.location.href = "/learnHanzi";
          }
        }
      },
      reviewLevel: {
        name: "Review Level",
        callback: function(key, opt){
          const currentLevelHanzi = getCurrentLevelHanzi('.knownHanzi', this);
          const previousLevelsHanzi = getPreviousLevelsHanzi(this);

          if(currentLevelHanzi === ""){
            alert('Please learn new Hanzi first.');
          } else {
            Cookies.set('currentLevelHanzi', currentLevelHanzi);
            Cookies.set('previousLevelsHanzi', previousLevelsHanzi);
            window.location.href = "/reviewLevel";
          }
        }
      }
    }
  });
});

function getCurrentLevelHanzi(selector, context) {
  let hanzi = "";
  $(selector, context).each(function(index, el) {
    hanzi += $(el).text();
  });

  return hanzi;
}

function getPreviousLevelsHanzi(context) {
  let hanzi = "";
  $(context).prevAll().each(function(index, el) {
    hanzi += $('.knownHanzi', el).text();
  });

  return hanzi;
}
