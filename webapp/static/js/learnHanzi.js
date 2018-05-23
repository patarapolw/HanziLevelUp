// $(document).ready(function() {
  var charList = '';
  var charNumber = 0;

  function previousChar(){
    if(charNumber > 0){
      charNumber--;
      renderChar();
    }
  }

  function nextChar(){
    if(charNumber + 1 < charList.length - 1){
      charNumber++;
      renderChar();
    }
  }

  function postChar(character){
    charList = character;
    charNumber = 0;
    renderChar();
  }

  charList = Cookies.get('allHanzi') || "";
  charNumber = 0;
  renderChar();

  $("#sentence").keypress(function(event) {
    if (event.which == 13) {
      charList = $('#sentence').val();
      charNumber = 0;
      renderChar();
    }
  });

  function renderChar(){
    var currentChar = charList[charNumber];
    var charToPost = currentChar;

    if(!isNaN(parseInt(charList))){
      $('#character').html('<div class="number">' + charList + '</div>');
      charToPost = charList;
    } else {
      $('#character').text(currentChar);
    }

    if(charNumber > 0){
      $('#previousChar').removeAttr('disabled');
    } else {
      $('#previousChar').attr('disabled', true);
    }
    if(charNumber + 1 < charList.length - 1){
      $('#nextChar').removeAttr('disabled');
    } else {
      $('#nextChar').attr('disabled', true);
    }

    $.post('/getHyperradicals', {character: charToPost}, function(content) {
      renderContent('#compositions', content.compositions);
      renderContent('#supercompositions', content.supercompositions);
      renderContent('#variants', content.variants);

      $('#vocab').text('');
      for(var i=0; i<content.vocab.length; i++){
        $('#vocab').append(
          "<div class='entry container'><a href='#' onclick='speak(\"{3}\"); return false;' title='{1}'>{0}</a> {2}</div>"
          .format(content.vocab[i][1],
            content.vocab[i][2],
            content.vocab[i][3],
            content.vocab[i][1].addSlashes()));
        }

      $('#sentences').text('');
      for(var i=0; i<content.sentences.length; i++){
        var speakerLang = (content.language == 'zh') ? 'zh-CN' : 'ja';
        $('#sentences').append(
          "<div class='entry container'><a href='#' onclick='speak(\"{2}\"); return false;'>{0}</a> {1}</div>"
          .format(content.sentences[i][0],
            content.sentences[i][1],
            stripHtml(content.sentences[i][0]).addSlashes()));
      }
    });
  }

  function speak(vocab){
    $.post('/speak', {sentence: vocab});
  }

  function renderContent(selector, contentList){
    $(selector).text('');
    for(var i=0; i<contentList.length; i++){
      var class_name = isNaN(parseInt(contentList[i])) ? 'character' : 'number';
      $(selector).append(
        "<div class='{0}' onclick='postChar(\"{1}\")'>{1}</div> "
          .format(class_name, contentList[i]));
    }
  }

  $(document).ajaxSend(function( event, xhr, settings ){
    if ( settings.url === "/getHyperradicals" ){
      $('.loading-container').show();
    }
  }).ajaxComplete(function( event, xhr, settings ){
    if ( settings.url === "/getHyperradicals" ){
      $('.loading-container').hide();
    }
  })
// });
