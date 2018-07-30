let charNumber = 0;
let charList = [];
let databaseCreated = false;

$(document).ready(function(){
  $('#input-search').keydown(function(event) {
    if (event.which == 13 || event.keyCode == 13) {
      doSubmit();
    }
  });

  $('#input-max-level').TouchSpin({
    min: 1,
    max: 100,
    mouse_wheel: true,
    buttondown_class: 'btn btn-outline-secondary',
    buttonup_class: 'btn btn-outline-secondary'
  }).change(function(){
    doSubmit();
  });

  $('#input-created')
    // .datetimepicker({
    //   date: moment().subtract(1, 'days'),
    //   format: 'YYYY-MM-DD HH:00'
    // });
    .val(moment().subtract(1, 'days').format('YYYY-MM-DD HH:00'))
    .datetimepicker({
      format: 'yyyy-mm-dd hh:00',
      todayBtn: true,
      todayHighlight: true,
      autoclose: true,
      minView: 'day',
      showMeridian: true
    })
    .change(function(){
      doSubmit();
    });

  $('#previousChar').click(function(){
    if(charNumber > 0){
      charNumber--;
      renderChar();
    }
  });

  $('#nextChar').click(function(){
    if(charNumber < charList.length - 1){
      charNumber++;
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

  setCharacterHoverListener($('#entry'));
  setCharacterHoverListener($('#variants'));

  init();
});

function init(){
  if(!databaseCreated){
    $.post('/post/quiz/index/hanzi', function(){
      databaseCreated = true;
      doSubmit();
    });
  }
}

function doSubmit(){
  if(!databaseCreated){
    init();
  } else {
    $.post('/post/quiz/read/hanzi', {
      search: $('#input-search').val(),
      level: $('#input-max-level').val(),
      created: $('#input-created').val()
    }, function(data){
      charNumber = 0;
      charList = data;

      console.log(data);

      $('#numberOfItems-all').text(data.length);

      renderChar();
    });
  }
}

function renderChar(){
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
  if(charList.length > 0){
    const currentEntry = charList[charNumber];

    $('#entry div').text(currentEntry.Hanzi);
    $('#level').text(currentEntry.Level);
    $('#pinyin').text(currentEntry.Pinyin);
    $('#english').text(currentEntry.English);

    $('#numberOfItems-current').text(charNumber + 1);

    const $variants = $('#variants');
    $variants.html("");
    for(let i=0; i<currentEntry.Variants.length; i++){
      $variants.append("<div class='{0}'>{1}</div> ".format('character', currentEntry.Variants[i]));
    }

    $.post('/post/hanzi/getInfo', {character: currentEntry.Hanzi}, function(content) {
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

    $.post('/post/hanzi/getSentences', {character: currentEntry.Hanzi}, function(content) {
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
      const win = window.open('https://tatoeba.org/eng/sentences/search?from=cmn&to=eng&query=' + currentEntry.Hanzi, '_blank');
      win.focus();
    });
  } else {
    $('#entry div').text("");
    $('#level').text("");
    $('#pinyin').text("");
    $('#english').text("");
    $('#variants').html("");
    $('#vocab').text("");
    $('#sentences').text("");
    $('#more-sentences').off('click')

    $('#numberOfItems-current').text(0);
  }
}
