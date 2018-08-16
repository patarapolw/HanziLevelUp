if(!show){
  document.getElementById('show-area').innerHTML = markdown2html(card.front, card);
} else {
  viewItem(markdown2html(card.back, card));
}

async function viewItem(itemValue){
  $.post('/post/item/cut', { item: itemValue }, function(data, textStatus, xhr) {
    const $showarea = $('#show-area');

    $showarea.html('');
    let $line = $('<div />');
    for(let i=0; i<data.length; i++){
      if(data[i] === '\n'){
        $showarea.append($line);
        $line = $('<div />');
      } else if(data[i] === ' '){
        $line.append('&nbsp;');
      } else {
        if(hasHanzi(data[i])){
          $line.append('<div class="entry inline"><div onclick="speak(\'{0}\')">{1}</div>'
            .format(stripHtml(data[i]), data[i]));
        } else {
          $line.append(data[i]);
        }
      }
    }
    $showarea.append($line);
  });
}
