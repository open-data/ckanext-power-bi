this.ckan.module('power-bi-embed', function($){
  return {
    /* options object can be extended using data-module-* attributes */
    options : {
      config: {},
    },
    initialize: function (){
      let reportContainer = $('#power-bi-container');

      if( reportContainer.length > 0 ){
        let interval = false;
        let tries = 0;
        const maxTries = 25;
        interval = setInterval(function(){
          console.log('Attempting to initialize PowerBI report...(' + tries + 1 + '/' + maxTries + ')');
          let reportObj = powerbi.embed(reportContainer[0], this.options.config);
          if( typeof reportObj != 'undefined' && typeof reportObj.config != 'undefined' ){
            console.log('Successfully initialized PowerBI report...');
            clearInterval(interval);
            interval = false;
            return;
          }
          if( tries > maxTries ){
            console.warn('Failed to initialize PowerBI report...');
            clearInterval(interval);
            interval = false;
            return;
          }
          tries++;
        }, 250);
      }else{
        console.warn('Unable to locate the element to embed the PowerBI report...');
      }

    }
  };
});
