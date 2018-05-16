var sentenceHTMLTemplate = '<div id="{0}">'
+ '<a class="float-right deleteSentence" href="#">x</a>'
+ '<div onclick="speak(\'{1}\')">{2}</div>'
+ '</div>';

$(document).ready(function() {
  $.post('/getSentence', function(data) {
    var all_sentences = data;
    for(var i=0; i<all_sentences.length; i++){
      $('#contents').prepend(sentenceHTMLTemplate.format(
        all_sentences[i][0],
        all_sentences[i][1].addSlashes(),
        all_sentences[i][1]));
    }
  });


  $('#sentenceInput').keydown(function(event) {
    if (event.which == 13 || event.keyCode == 13) {
      var sentence = $(this).val();
      $.post('/addSentence', { sentence: sentence }, function(sentence_id){
        $('#contents').prepend(sentenceHTMLTemplate.format(sentence_id, sentence.addSlashes(), sentence));
      });
    }
  });

  $('.deleteSentence').click(function(){
    $.post('/deleteSentence', { sentence_id: $(this).parent().attr('id') });
    $(this).parent().remove();

    return false;
  });
});

function speak(sentence){
  $.post('/speak', { sentence: sentence });
}
