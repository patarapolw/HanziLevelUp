let vocabList = localStorage.getObject('allVocab') || [];
let vocabNumber = 0;
let vocabInfoArray;
let previousVocab = "";

console.log(vocabList);

$(document).ready(function() {
  initVocab();

  $("#input-vocab").keypress(function(event) {
    if (event.which == 13) {
      vocabList = [$(this).val()];
      initVocab();
    }
  });
});

async function initVocab(){
  vocabNumber = 0;

  await $.post('/post/vocab/getListInfo', {list: JSON.stringify(vocabList)}, function(getListInfo) {
    vocabInfoArray = getListInfo;
  });

  loadVocabInfo();
}

async function loadVocabInfo(){
  const currentVocab = vocabInfoArray[vocabNumber];

  $('#traditional > div').first().text(currentVocab.traditional);
  $('#simplified > div').first().text(currentVocab.simplified);
  $('#reading').text(currentVocab.pinyin);
  $('#meaning').text(currentVocab.english);

  if(vocabNumber > 0){
    $('#previous-button').removeAttr('disabled');
  } else {
    $('#previous-button').attr('disabled', true);
  }
  if(vocabNumber < vocabInfoArray.length - 1){
    $('#next-button').removeAttr('disabled');
  } else {
    $('#next-button').attr('disabled', true);
  }

  if(currentVocab.simplified !== previousVocab){
    $.post('/post/vocab/getSentences', { vocab: currentVocab.simplified }, function(sentences) {
      const $sentences = $('#sentences');
      $sentences.text('');
      for(let i=0; i<sentences.length; i++){
        $sentences.append(
          "<div class='entry container'><a href='#' onclick='speak(\"{2}\"); return false;'>{0}</a> {1}</div>"
          .format(sentences[i].sentence,
            sentences[i].english,
            stripHtml(sentences[i].sentence).addSlashes()));
      }

      $('#sentences').contextMenu({
        selector: ".entry",
        build: function($trigger, e) {
          return contextMenuBuilder($trigger, e, 'sentence', 'a')
        }
      });
    });

    $('#more-sentences').off('click').click(function(event) {
      event.preventDefault();
      console.log(currentVocab);
      const win = window.open('https://tatoeba.org/eng/sentences/search?from=cmn&to=eng&query=' + currentVocab[1], '_blank');
      win.focus();
    });
  }

  $('#simplified-container').contextMenu({
    selector: '.vocab',
    build: function($trigger, e) {
      return contextMenuBuilder($trigger, e, 'vocab', 'div')
    }
  });

  $('#traditional-container').contextMenu({
    selector: '.vocab',
    build: function($trigger, e) {
      return contextMenuBuilder($trigger, e, 'vocab', 'div')
    }
  });

  $('#simplified > div').off('click').click(function(event) {
    speak($(this).text());
  });

  $('#traditional > div').off('click').click(function(event) {
    speak($(this).text());
  });

  previousVocab = currentVocab.simplified;
}

function loadPrev(){
  if(vocabNumber > 0){
    vocabNumber--;
    loadVocabInfo();
  }
}

function loadNext(){
  if(vocabNumber < vocabInfoArray.length - 1){
    vocabNumber++;
    loadVocabInfo();
  }
}

$(document).ajaxSend(function( event, xhr, settings ){
  $('.loading-container').show();
}).ajaxComplete(function( event, xhr, settings ){
  $('.loading-container').hide();
});
