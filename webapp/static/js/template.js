$(document).ready(function() {
  setTextSync();

  $('#sync-default').click(function(event) {
    doSync();
  });

  $('#sync-anki').click(function(event) {
    event.preventDefault();
    setTextSync('anki');
    doSync('anki');
  });

  $('#sync-kitsun').click(function(event) {
    event.preventDefault();
    setTextSync('kitsun');
    doSync('kitsun');
  });

  $('#export-csv').click(function(event) {
    event.preventDefault();
    doExport('csv');
  });
});

function setTextSync(syncType){
  if(syncType === undefined){
    syncType = localStorage.getItem('syncType') || 'anki';
  }
  localStorage.setItem('syncType', syncType);

  $('#text-sync').text($('#sync-' + syncType).text());
}

function doSync(){
  const syncType = localStorage.getItem('syncType') || 'anki';
  const $spinner = $('#spinner-sync');

  $spinner.addClass('fa-spin');
  $.post('/post/sync/' + syncType, function(data, textStatus, xhr) {
    if(data === '0'){
      alert('Syncing failed');
    }
    $spinner.removeClass('fa-spin');
  });
}

function doExport(exportType){
  const $spinner_sync = $('#spinner-sync');
  const $spinner_export = $('#spinner-export');

  $spinner_sync.hide();
  $spinner_export.show();

  $.post('/post/export/' + exportType, function(data, textStatus, xhr) {
    if(data === '0'){
      alert('Exporting failed');
    } else {
      let filename;
      switch (exportType) {
        case 'csv':
          filename = 'Chinese.zip';
          break;
        default:
          filename = 'Chinese.zip';
      }
      downloadURI('/get/export/' + filename);
    }
    $spinner_sync.show();
    $spinner_export.hide();
  });
}

function downloadURI(uri, name)
{
    var link = document.createElement("a");
    link.download = name;
    link.href = uri;
    link.click();
}
