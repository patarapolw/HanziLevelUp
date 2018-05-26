var charList = '';
var charNumber = 0;

$(document).ready(function() {
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

  $(document).ajaxSend(function( event, xhr, settings ){
    if ( settings.url === "/getHyperradicals" ){
      $('.loading-container').show();
    }
  }).ajaxComplete(function( event, xhr, settings ){
    if ( settings.url === "/getHyperradicals" ){
      $('.loading-container').hide();
    }
  })

  $('#vocab').contextMenu({
    selector: ".entry",
    build: function($trigger, e) {
      const vocab = $trigger.children('a').text();

      async function loadMenu(){
        const vocabInLearning = await $.post('/vocabInLearning', { vocab: vocab });
        const isLearnt = (parseInt(vocabInLearning) > 0);

        $('.context-menu-item > span').each(function(index, el) {
          var $this = $(this);
          switch($this.text()){
            case 'Loading':
              $this.parent().hide();
              break;
            case 'Add to learning':
              if(isLearnt <= 0){
                $this.parent().show();
              }
              break;
            case 'Remove from learning':
              if(isLearnt > 0){
                $this.parent().show();
              }
              break;
          }
        });
      }

      loadMenu();

      return {
        items: {
          loading: {
            name: 'Loading',
            visible: true
          },
          addToLearning: {
            name: "Add to learning",
            visible: false,
            callback: function(key, opt){
              $.post('/addVocabToLearning', { vocab: vocab });
            }
          },
          removeFromLearning: {
            name: "Remove from learning",
            visible: false,
            callback: function(key, opt){
              $.post('/removeVocabFromLearning', { vocab: vocab });
            }
          }
        }
      };
    }
  });

  $('#sentences').contextMenu({
    selector: ".entry",
    build: function($trigger, e) {
      const sentence = $trigger.children('a').text();

      async function loadMenu(){
        const sentenceInLearning = await $.post('/sentenceInLearning', { sentence: sentence });
        const isLearnt = (parseInt(sentenceInLearning) > 0);

        $('.context-menu-item > span').each(function(index, el) {
          var $this = $(this);
          switch($this.text()){
            case 'Loading':
              $this.parent().hide();
              break;
            case 'Add to learning':
              if(isLearnt <= 0){
                $this.parent().show();
              }
              break;
            case 'Remove from learning':
              if(isLearnt > 0){
                $this.parent().show();
              }
              break;
          }
        });
      }

      loadMenu();

      return {
        items: {
          loading: {
            name: 'Loading',
            visible: true
          },
          addToLearning: {
            name: "Add to learning",
            visible: false,
            callback: function(key, opt){
              $.post('/addSentenceToLearning', { sentence: sentence });
            }
          },
          removeFromLearning: {
            name: "Remove from learning",
            visible: false,
            callback: function(key, opt){
              $.post('/removeSentenceFromLearning', { sentence: sentence });
            }
          }
        }
      };
    }
  });
});

function previousChar(){
  if(charNumber > 0){
    charNumber--;
    renderChar();
  }
}

function nextChar(){
  if(charNumber < charList.length - 1){
    charNumber++;
    renderChar();
  }
}

function postChar(character){
  charList = character;
  charNumber = 0;
  renderChar();
}

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
  if(charNumber < charList.length - 1){
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
