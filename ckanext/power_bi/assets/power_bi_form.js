window.addEventListener('load', function(){
  $(document).ready(function() {
    let publicReportField = $('input#field-public_report');
    let publicReportFields = $('div.public-report-field');
    if( publicReportField.length > 0 && publicReportFields.length > 0 ){
      function _show_public_report_fields(do_animate){
        let cascade = 0;
        let timing = 0;
        if( do_animate ){
          timing = 635;
        }
        if( $(publicReportField).is(':checked') ){
          $(publicReportFields).each(function(_index, _element){
            if( do_animate ){
              setTimeout(function(){
                $(_element).show(timing);
              }, cascade);
              cascade += timing;
            }else{
              $(_element).show(timing);
            }
          });
        }else{
          $(publicReportFields).each(function(_index, _element){
            $(_element).hide(timing);
          });
        }
      }
      _show_public_report_fields(false);
      $(publicReportField).off('change.ShowHide');
      $(publicReportField).on('change.ShowHide', function(_event){
        _show_public_report_fields(true);
      });
    }
  });
});
