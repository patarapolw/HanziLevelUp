var vocabFloatingHTMLTemplate = '<div id="{0}" class="floating">'
+ '<div onclick="speak(\'{1}\')">{2}</div>'
+ '</div>';

var vocabHTMLTemplate = '<div id="{0}" class="entry">'
+ '<a class="float-left deleter" href="#">x</a> '
+ '<div onclick="speak(\'{1}\')">{2}</div>'
+ '</div>';

$(document).ready(function() {
  itemLoader();

  $('#vocabInput').keydown(function(event) {
    if (event.which == 13 || event.keyCode == 13) {
      var vocab = $(this).val();
      $.post('/addVocab', { vocab: vocab }, function(vocab_id){
        $('#contents').prepend(vocabHTMLTemplate.format(vocab_id, vocab.addSlashes(), vocab));
        setDeleteVocabListener();
      });
    }
  });
});

async function itemLoader(){
  var recentVocabId = [];

  await $.post('/getRecentVocab', function(recent_vocab) {
    var $contents = $('#contents');

    for(var i=0; i<recent_vocab.length; i++){
      $contents.append(vocabHTMLTemplate.format(
        recent_vocab[i][0],
        recent_vocab[i][1].addSlashes(),
        recent_vocab[i][1]));
      recentVocabId.push(recent_vocab[i][0]);
    }

    setDeleteVocabListener();
  });

  await $.post('/getAllVocab', function(all_vocab) {
    var usedCoordinate = [];
    var failedObject = [];
    var $showcase = $('#showcase');
    var $showcaseWidth = $showcase.width() - 20;
    var $showcaseHeight = $showcase.height() - 20;
    var showcaseCoordinate = {
      offset: $showcase.offset(),
      height: $showcase.height(),
      width: $showcase.width()
    };

    for(var i=0; i<all_vocab.length; i++){
      if(recentVocabId.indexOf(all_vocab[i][0]) !== -1){
        continue;
      }

      if(failedObject.length > 10){
        break;
      }

      $showcase.append(vocabFloatingHTMLTemplate.format(
        all_vocab[i][0],
        all_vocab[i][1].addSlashes(),
        all_vocab[i][1]));

      var currentVocab = $('#' + all_vocab[i][0]);
      currentVocab.css({
        'position': 'absolute',
        'left': Math.random()*$showcaseWidth + 10,
        'top': Math.random()*$showcaseHeight + 10
      });

      var currentCoordinate = {
        offset: currentVocab.offset(),
        height: currentVocab.height(),
        width: currentVocab.width()
      };

      function isOverlap_current(el1){
        return isOverlap(currentCoordinate, el1);
      }

      if(usedCoordinate.some(isOverlap_current) ||
          currentCoordinate.offset.left < showcaseCoordinate.offset.left ||
          currentCoordinate.offset.top + currentCoordinate.height > showcaseCoordinate.offset.top + showcaseCoordinate.height){
        currentVocab.remove();
        failedObject.push(currentVocab.text());
      } else {
        usedCoordinate.push(currentCoordinate);
      }
    }
  });
}

function setDeleteVocabListener(){
  $('.deleter').click(function(){
    $.post('/deleteVocab', { vocab_id: $(this).parent().attr('id') });
    $(this).parent().remove();

    return false;
  });
}

function loadHanzi(){
  $.post('/vocabToHanzi', function(data, textStatus, xhr) {
    Cookies.set('allHanzi', data);
    window.location.href = '/learnHanzi';
  });
}
