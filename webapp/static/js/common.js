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

Storage.prototype.setObject = function(key, value) {
    this.setItem(key, JSON.stringify(value));
}

Storage.prototype.getObject = function(key) {
    var value = this.getItem(key);
    return value && JSON.parse(value);
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
    let currentCoordinate;
    let doLoop = true;

    while (doLoop) {
      doLoop = false;
      // console.log('Placing item:', allItems[i][1]);

      currentItem.css({
        'left': Math.random()*$showcaseWidth,
        'top': Math.random()*$showcaseHeight
      });

      if(currentItem.width() < preferredWidth){
        console.log(currentItem.width(), preferredWidth);
        doLoop = true;
        continue;
      }

      currentItem.data('offset', currentItem.offset());
      currentItem.data('dimension', {
        height: currentItem.height(),
        width: preferredWidth
      })

      currentCoordinate = {
        offset: currentItem.data('offset'),
        height: currentItem.height(),
        width: currentItem.width()
      };

      if(currentCoordinate.offset.left < showcaseCoordinate.offset.left ||
          currentCoordinate.offset.top + currentCoordinate.height > showcaseCoordinate.offset.top + showcaseCoordinate.height){
        doLoop = true;
        continue;
      }
    }

    if(usedCoordinate.some(el => isOverlap(currentCoordinate, el))){
      failedObject.push(currentItem.attr('id'));
      currentItem.remove();
    } else {
      usedCoordinate.push(currentCoordinate);
    }
  }

  console.log('Items not shown:', failedObject);

  $('.floating').mouseenter(function(){
    const $this = $(this);
    const dimension = $this.data('dimension');
    const ratioEnlarged = 2;

    const tempElement = $this.clone();
    tempElement.appendTo('body');
    tempElement.css({
      width: dimension.width,
      height: dimension.height
    });

    if(tempElement.is(':offscreen')){
      // Change this to animate if you want it animated.
      $this.css({
        'margin-left': -dimension.width * ratioEnlarged/2,
        'margin-top': -dimension.height * ratioEnlarged/4,
        'font-size': ratioEnlarged + 'em',
        width: dimension.width * ratioEnlarged,
        height: dimension.height * ratioEnlarged
      });
    } else {
      $this.css({
        'margin-left': -dimension.width * ratioEnlarged/4,
        'margin-top': -dimension.height * ratioEnlarged/4,
        'font-size': ratioEnlarged + 'em',
        width: dimension.width * ratioEnlarged,
        height: dimension.height * ratioEnlarged
      });
    }

    tempElement.remove();
  });

  $('.floating').mouseleave(function(event) {
    const $this = $(this);
    const dimension = $this.data('dimension');

    if(!$this.hasClass('context-menu-active')){
      $this.css({
        margin: 0,
        'font-size': '1em',
        width: dimension.width,
        height: dimension.height
      });
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
        const dimension = $this.data('dimension');

        $this.css({
          margin: 0,
          'font-size': '1em',
          width: dimension.width,
          height: dimension.height
        });
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
        // case 'Generated from sentences':
        //   if(itemId <= 0){
        //     $this.parent().show();
        //   }
      }
    });
  }

  loadMenu();

  return {
    items: {
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
      learnHanzi: {
        name: "Learn Hanzi in this item",
        visible: true,
        callback: function(key, opt){
          sessionStorage.setItem('allHanzi', $trigger.children(childrenType).text());
          const win = window.open('/viewHanzi', '_blank');
          win.focus();
        }
      },
      learnVocab: {
        name: "Learn vocab in this item",
        visible: true,
        callback: function(key, opt){
          const win = window.open('about:blank', '_blank');
          loadVocabFromItem(itemType, $trigger.children(childrenType).text()).then(function(){
            win.location.href = '/viewVocab';
            win.focus();
          });
        }
      }
    }
  };
}

async function loadVocabFromItem(itemType, item){
  let allVocab;

  if(itemType === 'vocab'){
    allVocab = [item];
  } else {
    allVocab = await $.post('/post/vocab/fromSentence', {sentence: item});
  }

  sessionStorage.setObject('allVocab', allVocab);
}

function setCharacterHoverListener(){
  $('.character, .number').mouseenter(function(){
    const $this = $(this);
    const hoverElement = $('<div class="hoverElement">');

    hoverElement.appendTo('#showpanel');
    hoverElement.append($this.clone());
    hoverElement.position({
      my: 'center',
      at: 'center',
      of: $this
    });

    hoverElement.mouseleave(function(event) {
      if(!hoverElement.hasClass('context-menu-active')){
        hoverElement.remove();
      }
    });
  });

  $('.hoverElement').mouseleave(function(event) {
    const hoverElement = $(this);

    if(!hoverElement.hasClass('context-menu-active')){
      hoverElement.remove();
    }
  });

  $('#showpanel').contextMenu({
    selector: '.hoverElement',
    items: {
      viewHanzi: {
        name: 'View Hanzi info',
        callback: function(key, opt){
          sessionStorage.setItem('allHanzi', $(this).text());
          const win = window.open('/viewHanzi', '_blank');
          win.focus();
        }
      }
    },
    events: {
      hide: function(options){
        $('.hoverElement').remove();
        return true;
      }
    }
  });
}

function speak(item){
  $.post('/post/speak', { item: item });
}

$(document).ready(function() {
  jQuery.expr.filters.offscreen = function(el) {
    var rect = el.getBoundingClientRect();
    return (
             (rect.x + rect.width) < 0
               || (rect.y + rect.height) < 0
               || (rect.x > window.innerWidth || rect.y > window.innerHeight)
           );
  };
});
