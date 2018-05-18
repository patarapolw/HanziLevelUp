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

function speak(sentence){
  $.post('/speak', { sentence: sentence });
}
