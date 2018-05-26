$(document).ready(function() {
  itemLoader();
});

async function itemLoader(){
  const currentLevelHanzi = Cookies.get('currentLevelHanzi') || "";
  const previousLevelsHanzi = Cookies.get('previousLevelsHanzi') || "";
  const hanziJson = {
    currentLevelHanzi: currentLevelHanzi,
    previousLevelsHanzi: previousLevelsHanzi
  };

  loadHanziView(currentLevelHanzi);

  $.post('/post/vocab/getLevel', hanziJson, function(levelVocab) {
    createAquarium('vocab', levelVocab);
  });
  $.post('/post/sentence/getLevel', hanziJson, function(levelSentences) {
    createAquarium('sentence', levelSentences);
  });
}

function loadHanziView(contentList){
  const $showpanel = $("#showpanel");

  $showpanel.text('');
  for(let i=0; i<contentList.length; i++){
    const class_name = isNaN(parseInt(contentList[i])) ? 'character' : 'number';

    $showpanel.append(
      "<div class='{0} levelHanzi'>{1}</div> "
        .format(class_name, contentList[i]));
  }

  $showpanel.contextMenu({
    selector: '.levelHanzi',
    items: {
      viewHyperradicals: {
        name: 'View Hyperradicals',
        callback: function(key, opt){
          Cookies.set('allHanzi', $(this).text());
          const win = window.open('/learnHanzi', '_blank');
          win.focus();
        }
      }
    }
  });
}
