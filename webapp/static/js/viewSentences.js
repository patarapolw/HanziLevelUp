const HTMLTemplate = '<div id="{0}" class="entry">'
+ '<a class="float-left deleter" href="#">x</a> '
+ '<div onclick="speak(\'{1}\')">{2}</div>'
+ '</div>';

$(document).ready(function() {
  itemLoader();
  setInputBoxListener();

  $('#recent-sentences').on('click', '.deleter', function(){
    $.post('/post/sentence/delete', { id: $(this).parent().attr('id') });
    $(this).parent().remove();

    return false;
  });
});

async function itemLoader(){
  let recentSentencesId = [];

  await $.post('/post/sentence/getRecent', function(recent_sentences) {
    const $recent = $('#recent-sentences');

    for(let i=0; i<recent_sentences.length; i++){
      $recent.append(HTMLTemplate.format(
        recent_sentences[i][0],
        recent_sentences[i][1].addSlashes(),
        recent_sentences[i][1]));
      recentSentencesId.push(recent_sentences[i][0]);
    }

    $recent.contextMenu({
      selector: ".entry",
      build: function($trigger, e) {
        return contextMenuBuilder($trigger, e, 'sentence', 'div')
      }
    });
  });

  await $.post('/post/sentence/getAll', function(all_sentences) {
    let validSentences = [];

    for(let i=0; i<all_sentences.length; i++){
      if(recentSentencesId.indexOf(all_sentences[i][0]) === -1){
        validSentences.push(all_sentences[i]);
      }
    }

    createAquarium('sentence', validSentences);
  });
}

function setInputBoxListener(){
  $('#sentenceInput').keydown(function(event) {
    if (event.which == 13 || event.keyCode == 13) {
      const sentence = $(this).val();
      $.post('/post/sentence/add', { item: sentence }, function(sentence_id){
        $('#recent-sentences').prepend(HTMLTemplate.format(sentence_id, sentence.addSlashes(), sentence));
      });
    }
  });
}

function loadHanzi(){
  $.post('/post/hanzi/fromSentence', function(data, textStatus, xhr) {
    sessionStorage.setItem('allHanzi', data);
    window.location.href = '/viewHanzi';
  });
}
