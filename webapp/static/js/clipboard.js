const HTMLTemplate = '<div id="{0}" class="entry {2}">'
+ '<a class="float-left deleter" href="#">x</a> '
+ '<div class="entry-content">{1}</div>'
+ '</div>';

$(document).ready(function() {
  itemLoader();
  setInputBoxListener();

  $('#recent-items').on('click', '.deleter', function(){
    const $item = $(this).parent();
    const params = {
      id: $item.attr('id'),
      type: $item.data('type'),
      item: $item.children('.entry-content').text().trim()
    };

    $.post('/post/{0}/delete'.format(params.type), params);
    $item.remove();
  }).on('click', '.entry-content', function(){
    $.post('/post/speak', { item: $(this).text() });
  })

  $('#itemShowarea').contextMenu({
    selector: ".entry",
    build: function($trigger, e) {
      return contextMenuBuilder($trigger, e, 'sentence', 'div');
    }
  });
});

async function itemLoader(){
  $.post('/post/item/getRecent', function(items) {
    const $recent = $('#recent-items');
    let recent = {
      vocab: [],
      sentence: []
    };

    for(let i=0; i<items.length; i++){
      const $item = $(HTMLTemplate.format(
        items[i][0],
        items[i][1],
        items[i][3]
      ));
      const $flair = $('<div class="flair {0} float-right">{0}</div>'.format(items[i][3]));

      $item.append($flair);
      $item.data('type', items[i][3]);
      $recent.append($item);

      const width = $item.children('.entry-content').width() - $flair.width();
      $item.children('.entry-content').width(width);

      recent[items[i][3]].push(removeAscii(items[i][1]));
    }

    showareaDefaultLoader(recent);

    $recent.contextMenu({
      selector: ".entry",
      build: function($trigger, e) {
        return contextMenuBuilder($trigger, e, $trigger.data('type'), 'div');
      }
    });
  });
}

function setInputBoxListener(){
  $('button').click(function(event) {
    const itemValue = $('#itemInput').val();
    viewItem(itemValue);

    const $button = $(this);
    const itemType = $button.attr('value');
    if(itemType !== 'sentence' && itemType !== 'vocab'){
      return false;
    }

    $.post('/post/{0}/add'.format(itemType), { item: itemValue }, function(item_id){
      const $item = $(HTMLTemplate.format(
        item_id,
        itemValue,
        itemType
      ));
      $item.data('type', itemType);
      // $recent.append($item);

      const $flair = $('<div class="flair {0} float-right">{0}</div>'.format(itemType));

      $item.append($flair);
      $('#recent-items').prepend($item);

      const $entryContent = $item.children('.entry-content');
      const width = $entryContent.width() - $flair.width();
      $entryContent.width(width);
    });
  });

  $('#itemInput').on('paste', function(e) {
    viewItem(e.originalEvent.clipboardData.getData('text'));
  });
}

async function viewItem(itemValue){
  $.post('/post/item/cut', { item: itemValue }, function(data, textStatus, xhr) {
    const $showarea = $('#itemShowarea');

    $showarea.html('');
    let $line = $('<div />');
    for(let i=0; i<data.length; i++){
      if(data[i] === '\n'){
        $showarea.append($line);
        $line = $('<div />');
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

function showareaDefaultLoader(recent){
  shuffleArray(recent.vocab);
  shuffleArray(recent.sentence);

  let output = 'Vocab: \n';
  for(let i=0; i<recent.vocab.length; i++){
    // if(i>=10){
    //   break;
    // }
    output += '* {0}  '.format(recent.vocab[i]);
  }

  output += '\nSentences: \n';
  for(let i=0; i<recent.sentence.length; i++){
    // if(i>=10){
    //   break;
    // }
    output += '* {0} \n'.format(recent.sentence[i]);
  }

  viewItem(output);
}
