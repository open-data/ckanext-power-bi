this.ckan.module('power-bi-embed', function($){
  return {
    /* options object can be extended using data-module-* attributes */
    options : {
      config: {},
    },
    initialize: function (){
      let reportContainer = $('#power-bi-container');
      let reportConfig = null;

      if( typeof this.options == 'undefined' || this.options == null ){
        console.log('Failed to load PowerBI configuration from module...generating new object...');
        reportConfig = JSON.parse($('[data-module="power-bi-embed"]').attr('data-module-config'));
      }else{
        reportConfig = this.options.config;
      }

      if( typeof reportConfig == 'undefined' || reportConfig == null || reportConfig.length == 0 ){
        console.warn('Failed to generate PowerBI configuration...');
        return;
      }

      if( reportContainer.length == 0 ){
        console.warn('Unable to locate the element to embed the PowerBI report...');
        return;
      }

      console.log('Attempting to initialize PowerBI report...');
      let reportObj = powerbi.embed(reportContainer[0], reportConfig);
      if( typeof reportObj == 'undefined' || reportObj == null ){
        console.warn('Failed to initialize PowerBI report...');
        return;
      }

      console.log('Successfully initialized PowerBI report...');

    }
  };
});
