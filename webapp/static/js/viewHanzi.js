let charList = sessionStorage.getObject('allHanzi') || [];
let charNumber = sessionStorage.getObject('allHanziNumber') || 0;

$(document).ready(function() {
  renderChar();

  $("#sentence").keypress(function(event) {
    if (event.which == 13) {
      charList = $('#sentence').val().split('');
      charNumber = 0;
      renderChar();
    }
  });

  $('#vocab').contextMenu({
    selector: ".entry",
    build: function($trigger, e) {
      return contextMenuBuilder($trigger, e, 'vocab', 'a')
    }
  });

  $('#sentences').contextMenu({
    selector: ".entry",
    build: function($trigger, e) {
      return contextMenuBuilder($trigger, e, 'sentence', 'a')
    }
  });

  setCharacterHoverListener($('#compositions'));
  setCharacterHoverListener($('#supercompositions'));
  setCharacterHoverListener($('#variants'));
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

function renderChar(){
  charList = charList.filter((x, pos, self) => ((hasHanzi(x) || !isNaN(parseInt(x))) && self.indexOf(x) == pos));

  const currentChar = charList[charNumber];

  if(isNaN(parseInt(currentChar))){
    $('#character').html(currentChar)
  } else {
    $('#character').html('<div class="big-number">{0}</div>'.format(currentChar));
    $('.big-number').position({
      my: 'center bottom',
      at: 'center bottom-30',
      of: '.big-character'
    });
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

  $.post('/post/hanzi/getInfo', {character: currentChar}, function(content) {
    renderContent('#compositions', content.compositions);
    renderContent('#supercompositions', content.supercompositions);
    renderContent('#variants', content.variants);

    const $vocab = $('#vocab');
    $vocab.text('');
    for(let i=0; i<content.vocab.length; i++){
      $vocab.append(
        "<div class='entry container'><a href='#' onclick='speak(\"{3}\"); return false;' title='{1}'>{0}</a> {2}</div>"
        .format(content.vocab[i][1],
          content.vocab[i][2],
          content.vocab[i][3],
          content.vocab[i][1].addSlashes()));
    }
  });

  $.post('/post/hanzi/getSentences', {character: currentChar}, function(content) {
    const $sentences = $('#sentences');
    $sentences.text('');
    for(let i=0; i<content.sentences.length; i++){
      $sentences.append(
        "<div class='entry container'><a href='#' onclick='speak(\"{2}\"); return false;'>{0}</a> {1}</div>"
        .format(content.sentences[i][0],
          content.sentences[i][1],
          stripHtml(content.sentences[i][0]).addSlashes()));
    }
  });

  $('#more-sentences').off('click').click(function(event) {
    event.preventDefault();
    const win = window.open('https://tatoeba.org/eng/sentences/search?from=cmn&to=eng&query=' + currentChar, '_blank');
    win.focus();
  });
}

function renderContent(selector, contentList){
  $(selector).text('');
  for(let i=0; i<contentList.length; i++){
    const class_name = isNaN(parseInt(contentList[i])) ? 'character' : 'number';
    $(selector).append(
      "<div class='{0}'>{1}</div> "
        .format(class_name, contentList[i]));
  }
}
