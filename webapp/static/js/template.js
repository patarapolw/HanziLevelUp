$(document).ready(function() {
  $('#sync-default').click(function(event) {
    doExport('excel');
  });

  $('.navbar-nav div')
    .mouseenter(function(){
      $(this).siblings().each(function(){
        $('.dropdown-menu', this).css('transition-delay', '0s');
      });
    })
    .mouseleave(function(){
      $(this).siblings().each(function(){
        $('.dropdown-menu', this).css('transition-delay', '0.2s');
      });
    });

  $('.pendingReview').hide();
});

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
        case 'excel':
          filename = 'HanziLevelUp.xlsx';
          break;
        default:
          filename = 'HanziLevelUp.zip';
      }
      alert('Exporting completed. Please view the file in "./user/' + filename + '".')
      // downloadURI('/get/export/' + filename);
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
