// First, checks if it isn't implemented yet.
if (!String.prototype.format) {
  String.prototype.format = function() {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) {
      return typeof args[number] != 'undefined'
        ? args[number]
        : match
      ;
    });
  };
}

if(!String.prototype.addSlashes) {
    String.prototype.addSlashes = function()
    {
       //no need to do (str+'') anymore because 'this' can only be a string
       return this.replace(/[\\"']/g, '\\$&').replace(/\u0000/g, '\\0');
    }
}

function stripHtml(html){
   var doc = new DOMParser().parseFromString(html, 'text/html');
   return doc.body.textContent || "";
}

function shuffle(a) {
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function isOverlap(el0, el1) {
  var elY0 = (el0.offset.top < el1.offset.top)? el0 : el1;
  var elY1 = (el0 != elY0)? el0 : el1;
  var yInstersection = (elY0.offset.top + elY0.height) - elY1.offset.top > 0;

  var elX0 = (el0.offset.left < el1.offset.left)? el0 : el1;
  var elX1 = (el0 != elX0)? el0 : el1;
  var xInstersection = (elX0.offset.left + elX0.width) - elX1.offset.left > 0;

  return (yInstersection && xInstersection);
}

function createAquarium(itemType, allItems){
  shuffle(allItems);

  const floatingHTMLTemplate = '<div id="{0}" class="floating">'
  + '<div onclick="speak(\'{1}\')">{2}</div>'
  + '</div>';

  let usedCoordinate = [];
  let failedObject = [];

  const $showcase = $('#showcase-{0}'.format(itemType));
  const $showcaseWidth = $showcase.width();
  const $showcaseHeight = $showcase.height();
  const showcaseCoordinate = {
    offset: $showcase.offset(),
    height: $showcase.height(),
    width: $showcase.width()
  };

  for(let i=0; i<allItems.length; i++){
    if(failedObject.length > 10){
      break;
    }

    $showcase.append(floatingHTMLTemplate.format(
      allItems[i][0],
      allItems[i][1].addSlashes(),
      allItems[i][1]));

    let currentItem = $('#' + allItems[i][0]);
    let preferredWidth = currentItem.width();

    currentItem.css({
      'left': Math.random()*$showcaseWidth,
      'top': Math.random()*$showcaseHeight
    });

    if(currentItem.width() < preferredWidth){
      failedObject.push(currentItem.attr('id'));
      currentItem.remove();
      continue;
    }

    currentItem.data('offset', currentItem.offset());

    let currentCoordinate = {
      offset: currentItem.data('offset'),
      height: currentItem.height(),
      width: currentItem.width()
    };

    function isOverlap_current(el1){
      return isOverlap(currentCoordinate, el1);
    }

    if(usedCoordinate.some(isOverlap_current) ||
        currentCoordinate.offset.left < showcaseCoordinate.offset.left ||
        currentCoordinate.offset.top + currentCoordinate.height > showcaseCoordinate.offset.top + showcaseCoordinate.height){
      failedObject.push(currentItem.attr('id'));
      currentItem.remove();
    } else {
      usedCoordinate.push(currentCoordinate);
    }
  }

  $('.floating').mouseover(function(){
    const $this = $(this);
    const actualWidth = $this.width();

    $('body').append('<div class="floating context-menu-active" id="temp">');
    const $temp = $('#temp');
    $temp.text($this.text());

    const preferredWidth = $temp.width();
    $temp.remove();

    if(actualWidth < preferredWidth){
      $this.css('left', parseInt($this.css('left')) + actualWidth - preferredWidth);
    }
  });

  $('.floating').mouseout(function(event) {
    const $this = $(this);
    if(!$this.hasClass('context-menu-active')){
      $this.offset($this.data('offset'));
    }
  });

  $showcase.contextMenu({
    selector: '.floating',
    build: function($trigger, e){
      return contextMenuBuilder($trigger, e, itemType, 'div');
    },
    events: {
      hide: function(options){
        const $this = $(this);
        $this.offset($this.data('offset'));
        return true;
      }
    }
  });
}

function contextMenuBuilder($trigger, e, itemType, childrenType) {
  const itemId = parseInt($trigger.attr('id')) || 1;
  const postJson = {
    item: $trigger.children(childrenType).text()
  };

  async function loadMenu(){
    const inLearningCountString = await $.post('/post/{0}/inLearning'.format(itemType), postJson);
    const inLearningCount = parseInt(inLearningCountString);

    $('.context-menu-item > span').each(function(index, el) {
      const $this = $(this);

      switch($this.text()){
        case 'Loading':
          $this.parent().hide();
          break;
        case 'Add to learning':
          if(inLearningCount <= 0 && itemId > 0){
            $this.parent().show();
          }
          break;
        case 'Remove from learning':
          if(inLearningCount > 0 && itemId > 0){
            $this.parent().show();
          }
          break;
        case 'Generated from sentences':
          if(itemId <= 0){
            $this.parent().show();
          }
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
          $.post('/post/{0}/addToLearning'.format(itemType), postJson);
        }
      },
      removeFromLearning: {
        name: "Remove from learning",
        visible: false,
        callback: function(key, opt){
          $.post('/post/{0}/removeFromLearning'.format(itemType), postJson);
        }
      },
      generatedFromSentences: {
        name: "Generated from sentences",
        visible: false
      }
    }
  };
}

function speak(item){
  $.post('/post/speak', { item: item });
}
