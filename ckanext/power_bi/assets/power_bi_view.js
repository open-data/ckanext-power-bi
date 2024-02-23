this.ckan.module('power-bi-embed', function($){
  return {
    /* options object can be extended using data-module-* attributes */
    options : {
      config: {},
    },
    initialize: function (){
      let reportContainer = $('#power-bi-container');

      if( reportContainer.length > 0 ){
        powerbi.embed(reportContainer[0], this.options.config);
      }

    }
  };
});
