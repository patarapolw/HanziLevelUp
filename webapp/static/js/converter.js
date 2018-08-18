const markdownConverter = new showdown.Converter;

function markdown2html(text, card, truncate){
  truncate = truncate || false;
  text = text.replace(/\n+/g, "\n\n");

  if(!('json' in card)){
    card.json = JSON.parse(card.data);
    card.data = JSON.stringify(card.json, null, 2);
    if(truncate){
      card.data = card.data.slice(0, 1000);
    }
    card.data = card.data.replace(/ /g, '&nbsp;');
  }

  text = sprintf(text, card);

  return markdownConverter.makeHtml(text);
}
