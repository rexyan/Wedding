'use strict';
$(function() {
  // search form
  var $gridProductHome1 = $('.js-product-masonry-layout-1').imagesLoaded( function() {
    $gridProductHome1.isotope({
      itemSelector: '.item',
      percentPosition: true,
      masonry: {
        columnWidth: '.grid-sizer'
      }
    });
  });
});