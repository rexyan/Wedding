'use strict';
$( document ).ready(function() {
var tpj = jQuery;
  var revapi8;
  tpj(document).ready(function() {
      if (tpj("#slider_1").revolution == undefined) {
          revslider_showDoubleJqueryError("#slider_1");
      } else {
          revapi8 = tpj("#slider_1").show().revolution({
              sliderType: "standard",
              jsFileLocation: "../../revolution/js/",
              sliderLayout: "fullscreen",
              fullScreenOffsetContainer:"header.header-style-3",
              delay: 9000,
              navigation: {
                  arrows:{enable:false},
                  bullets: {enable:false},
              },      
              parallax: {
                type:"mouse",
                origo:"slidercenter",
                speed:2000,
                levels:[2,3,4,5,6,7,12,16,10,50],
              },
              responsiveLevels:[1920,991,767,481],
              gridwidth:[1170,768,481,480],
              gridheight:[745,745,745,745]                     
              
          });
      }
  }); /*ready*/
});