const HTMLTemplate = '<div id="{0}" class="entry">'
+ '<a class="float-left deleter" href="#">x</a> '
+ '<div onclick="speak(\'{1}\')">{2}</div>'
+ '</div>';

$(document).ready(function() {
  itemLoader();
  setInputBoxListener();
});

async function itemLoader(){
  var recentVocabId = [];

  await $.post('/post/vocab/getRecent', function(recent_vocab) {
    var $contents = $('#contents');

    for(var i=0; i<recent_vocab.length; i++){
      $contents.append(HTMLTemplate.format(
        recent_vocab[i][0],
        recent_vocab[i][1].addSlashes(),
        recent_vocab[i][1]));
      recentVocabId.push(recent_vocab[i][0]);
    }

    setDeleteVocabListener();
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
        $('#contents').prepend(HTMLTemplate.format(vocab_id, vocab.addSlashes(), vocab));
        setDeleteVocabListener();
      });
    }
  });
}

function setDeleteVocabListener(){
  $('.deleter').click(function(){
    $.post('/post/vocab/delete', { id: $(this).parent().attr('id') });
    $(this).parent().remove();

    return false;
  });
}

function loadHanzi(){
  $.post('/post/hanzi/fromVocab', function(data, textStatus, xhr) {
    Cookies.set('allHanzi', data);
    window.location.href = '/learnHanzi';
  });
}
