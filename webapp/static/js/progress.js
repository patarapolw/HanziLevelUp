$(document).ready(function() {
  loader();

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
            sessionStorage.setItem('allHanzi', allHanzi);
            window.location.href = "/viewHanzi";
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
            sessionStorage.setItem('allHanzi', allHanzi);
            window.location.href = "/viewHanzi";
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
            sessionStorage.setItem('currentLevelHanzi', currentLevelHanzi);
            sessionStorage.setItem('previousLevelsHanzi', previousLevelsHanzi);
            window.location.href = "/viewLevel";
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

function getRemainingHanzi(knownHanzi){
  let allHanzi = "";
  $('.entry').each(function(index, el) {
    allHanzi += $('.knownHanzi, .notKnownHanzi', el).text();
  });

  let remainingHanzi = [];
  for(let i=0; i<knownHanzi.length; i++){
    if(allHanzi.indexOf(knownHanzi[i]) === -1){
      remainingHanzi.push(knownHanzi[i]);
    }
  }
  return remainingHanzi;
}

async function loader(){
  $.post('/post/hanzi/getAll', function(knownHanzi) {
    $.post('/post/file/getLevels', function(hanziLevelsRaw) {
      const hanziLevels = hanziLevelsRaw.trim().split('\n');

      let level = 0;
      const maxLevelDisplayed = 60;
      for(let i=0; i<hanziLevels.length; i++){
        if(level >= maxLevelDisplayed - 1){
          break;
        }
        const element = $('<tr></tr>');

        if(hanziLevels[i].match(/\p{UIdeo}/u) !== null){
          level++;
          element.append('<td class="levelColumn">{0}</td>'.format(level));
          const td = $('<td class="hanziColumn"></td>');
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
          element.append('<th colspan="2">{0}</th>'.format(hanziLevels[i]));
        }
        $('.hanziShowcase').append(element);
      }

      $('.hanziShowcase').append('<th colspan="2">{0}</th>'.format('Extra'));

      const element = $('<tr></tr>');
      const td = $('<td class="hanziColumn extraHanzi" colspan="2"></td>');
      const hanziInLevel = getRemainingHanzi(knownHanzi);
      const hanziClass = "knownHanzi";
      for(let j=0; j<hanziInLevel.length; j++){
        td.append('<div class="hanzi {1}">{0}</div>'.format(hanziInLevel[j], hanziClass));
      }
      element.append(td);
      element.addClass('entry');
      $('.hanziShowcase').append(element);
    });
  });
}
