'use strict';
$(function() {
  var $gridProductHome1 = $('.js-product-masonry-3-columns-wrapper').imagesLoaded( function() {
    $gridProductHome1.isotope({
      itemSelector: '.item',
      percentPosition: true
    });
  });
});