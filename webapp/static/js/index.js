var sentenceFloatingHTMLTemplate = '<div id="{0}" class="floating">'
+ '<div onclick="speak(\'{1}\')">{2}</div>'
+ '</div>';

var sentenceHTMLTemplate = '<div id="{0}" class="entry">'
+ '<a class="float-left deleter" href="#">x</a> '
+ '<div onclick="speak(\'{1}\')">{2}</div>'
+ '</div>';

$(document).ready(function() {
  itemLoader();

  $('#sentenceInput').keydown(function(event) {
    if (event.which == 13 || event.keyCode == 13) {
      var sentence = $(this).val();
      $.post('/addSentence', { sentence: sentence }, function(sentence_id){
        $('#contents').prepend(sentenceHTMLTemplate.format(sentence_id, sentence.addSlashes(), sentence));
        setDeleteSentenceListener();
      });
    }
  });
});

async function itemLoader(){
  var recentSentencesId = [];

  await $.post('/getRecentSentences', function(recent_sentences) {
    var $contents = $('#contents');

    for(var i=0; i<recent_sentences.length; i++){
      $contents.append(sentenceHTMLTemplate.format(
        recent_sentences[i][0],
        recent_sentences[i][1].addSlashes(),
        recent_sentences[i][1]));
      recentSentencesId.push(recent_sentences[i][0]);
    }

    setDeleteSentenceListener();
  });

  await $.post('/getAllSentences', function(all_sentences) {
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

    for(var i=0; i<all_sentences.length; i++){
      if(recentSentencesId.indexOf(all_sentences[i][0]) !== -1){
        continue;
      }

      if(failedObject.length > 10){
        break;
      }

      $showcase.append(sentenceFloatingHTMLTemplate.format(
        all_sentences[i][0],
        all_sentences[i][1].addSlashes(),
        all_sentences[i][1]));

      var currentSentence = $('#' + all_sentences[i][0]);
      currentSentence.css({
        'position': 'absolute',
        'left': Math.random()*$showcaseWidth + 10,
        'top': Math.random()*$showcaseHeight + 10
      });

      var currentCoordinate = {
        offset: currentSentence.offset(),
        height: currentSentence.height(),
        width: currentSentence.width()
      };

      function isOverlap_current(el1){
        return isOverlap(currentCoordinate, el1);
      }

      if(usedCoordinate.some(isOverlap_current) ||
          currentCoordinate.offset.left < showcaseCoordinate.offset.left ||
          currentCoordinate.offset.top + currentCoordinate.height >
          showcaseCoordinate.offset.top + showcaseCoordinate.height ||
          currentCoordinate.offset.left + currentCoordinate.width > showcaseCoordinate.offset.left + showcaseCoordinate.width){
        currentSentence.remove();
        failedObject.push(currentSentence.text());
      } else {
        usedCoordinate.push(currentCoordinate);
      }
    }
  });
}

function setDeleteSentenceListener(){
  $('.deleter').click(function(){
    $.post('/deleteSentence', { sentence_id: $(this).parent().attr('id') });
    $(this).parent().remove();

    return false;
  });
}

function loadHanzi(){
  $.post('/sentenceToHanzi', function(data, textStatus, xhr) {
    Cookies.set('allHanzi', data);
    window.location.href = '/learnHanzi';
  });
}
