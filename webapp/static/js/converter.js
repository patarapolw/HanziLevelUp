const markdownConverter = new showdown.Converter;

function markdown2html(text, card){
  text = text.replace(/\n+/g, "\n\n");

  if(!('json' in card)){
    card.json = JSON.parse(card.data);
    card.data = JSON.stringify(card.json, null, 2);
  }

  text = sprintf(text, card);

  return markdownConverter.makeHtml(text);
}
