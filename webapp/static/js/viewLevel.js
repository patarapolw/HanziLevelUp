$(document).ready(function() {
  itemLoader();
});

async function itemLoader(){
  const currentLevelHanzi = sessionStorage.getObject('currentLevelHanzi') || [];
  const previousLevelsHanzi = sessionStorage.getObject('previousLevelsHanzi') || [];
  const hanziJson = {
    currentLevelHanzi: currentLevelHanzi.join(''),
    previousLevelsHanzi: previousLevelsHanzi.join('')
  };

  console.log(currentLevelHanzi, previousLevelsHanzi)
  loadHanziView(currentLevelHanzi);

  $.post('/post/vocab/getLevel', hanziJson, function(levelVocab) {
    createAquarium('vocab', levelVocab);
  });
  $.post('/post/sentence/getLevel', hanziJson, function(levelSentences) {
    createAquarium('sentence', levelSentences);
  });
}

function loadHanziView(contentList){
  const $showPanel = $("#showpanel");

  $showPanel.text('');
  for(let i=0; i<contentList.length; i++){
    $showPanel.append(
      "<div class='character'>{0}</div> "
        .format(contentList[i]));
  }

  setCharacterHoverListener($showPanel);
}
