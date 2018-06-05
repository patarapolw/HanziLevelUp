$(document).ready(function() {
  itemLoader();
});

async function itemLoader(){
  const currentLevelHanzi = sessionStorage.getItem('currentLevelHanzi') || "";
  const previousLevelsHanzi = sessionStorage.getItem('previousLevelsHanzi') || "";
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
    $showpanel.append(
      "<div class='character'>{0}</div> "
        .format(contentList[i]));
  }

  setCharacterHoverListener();
}
