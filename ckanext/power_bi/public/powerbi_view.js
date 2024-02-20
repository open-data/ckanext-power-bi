this.ckan.module('power-bi-embed', function($){
  return {
    /* options object can be extended using data-module-* attributes */
		options : {
			language: "en",
      config: {},
		},
    initialize: function (){
      let reportContainer = $('#power-bi-container');
      // {
      //   "type": "report",
      //   "tokenType": 1,
      //   "accessToken": "",
      //   "embedUrl": "",
      //   "id": "",
      //   "permissions": 7,
      //   "settings": {
      //     "allowfullscreen": true,
      //     "localSettings": {
      //       "language": this.options.language,
      //       "formatLocale": "CA"
      //     },
      //     "filterPaneEnabled": true,
      //     "navContentPaneEnabled": true
      //   }
      // }

      if( reportContainer.length > 0 ){
        powerbi.embed(reportContainer[0], this.options.config);
      }

    }
  };
});
