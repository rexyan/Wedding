'use strict';
$(function() {
  var $gridProductHome1 = $('.js-post-masonry-3-columns-wrapper').imagesLoaded( function() {
    $gridProductHome1.isotope({
      itemSelector: '.post',
      percentPosition: true
    });
  });
});