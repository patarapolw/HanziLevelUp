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
    data.forEach((item, index)=>{
      if(item === '\n'){
        $showarea.append($line);
        $line = $('<div />');
      } else if(item === ' '){
        $line.append('&nbsp;');
      } else {
        if(hasHanzi(item)){
          $line.append('<div class="entry inline"><div onclick="speak(\'{0}\')">{1}</div>'
            .format(stripHtml(item), item));
        } else {
          $line.append(item);
        }
      }
    });
    $showarea.append($line);
  });
}
