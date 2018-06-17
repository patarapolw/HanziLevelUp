const HTMLTemplate = '<div id="{0}" class="entry">'
+ '<a class="float-left deleter" href="#">x</a> '
+ '<div class="speak">{1}</div>'
+ '</div>';

$(document).ready(function() {
  itemLoader();
  setInputBoxListener();

  $('#recent-vocab').on('click', '.deleter', function(){
    $.post('/post/vocab/delete', { id: $(this).parent().attr('id') });
    $(this).parent().remove();

    return false;
  });

  $('#recent-vocab').on('click', '.speak', function(){
    $.post('/post/speak', { item: $(this).text() });
  })
});

async function itemLoader(){
  let recentVocabId = [];

  await $.post('/post/vocab/getRecent', function(recent_vocab) {
    const $recent = $('#recent-vocab');

    for(let i=0; i<recent_vocab.length; i++){
      $recent.append(HTMLTemplate.format(
        recent_vocab[i][0],
        recent_vocab[i][1]));
      recentVocabId.push(recent_vocab[i][0]);
    }

    $recent.contextMenu({
      selector: ".entry",
      build: function($trigger, e) {
        return contextMenuBuilder($trigger, e, 'vocab', 'div')
      }
    });
  });

  await $.post('/post/vocab/getAll', function(all_vocab) {
    let validVocab = [];

    for(let i=0; i<all_vocab.length; i++){
      if(recentVocabId.indexOf(all_vocab[i][0]) === -1){
        validVocab.push(all_vocab[i]);
      }
    }

    createAquarium('vocab', validVocab);
  });
}

function setInputBoxListener(){
  $('#vocabInput').keydown(function(event) {
    if (event.which == 13 || event.keyCode == 13) {
      var item = $(this).val();
      $.post('/post/vocab/add', { item: item }, function(vocab_id){
        $('#recent-vocab').prepend(HTMLTemplate.format(vocab_id, item));
      });
    }
  });
}
