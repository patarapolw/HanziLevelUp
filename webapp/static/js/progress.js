$(document).ready(function() {
  $.post('/getHanzi', function(knownHanzi) {
    $.post('/getLevels', function(hanziLevelsRaw) {
      var hanziLevels = hanziLevelsRaw.trim().split('\n');
      var level = 0;
      for(var i=0; i<hanziLevels.length; i++){
        var element = $('<tr></tr>');
        if(hanziLevels[i].match(/\p{UIdeo}/u) !== null){
          level++;
          element.append('<td style="text-align: right;">{0}</td>'.format(level));
          var td = $('<td></td>');
          var hanziInLevel = hanziLevels[i].split("");
          for(j=0; j<hanziInLevel.length; j++){
            var hanziClass;
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
          if(!loadHanzi('.notKnownHanzi', this)){
            alert('All Hanzi in this level are learnt.');
          }
        }
      },
      reviewHanzi: {
        name: "Review Hanzi",
        callback: function(key, opt){
          if(!loadHanzi('.knownHanzi', this)){
            alert('Please learn new Hanzi first.');
          }
        }
      }
    }
  });
});

function loadHanzi(selector, context) {
  var allHanzi = "";
  $(selector, context).each(function(index, el) {
    allHanzi += $(el).text();
  });

  if(allHanzi !== ""){
    Cookies.set('allHanzi', allHanzi);
    window.location.href = "/learnHanzi";
  } else {
    return false;
  }

  return true;
}
