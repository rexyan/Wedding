'use strict';
$(function() {
   $('.main-carousel').slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows: true,
    fade: true,
    asNavFor: '.thumbnail-carousel',
    nextArrow: '<div class="carousel-arrow prev"><span class="lnr lnr-chevron-left"></span></div>',
    prevArrow: '<div class="carousel-arrow next"><span class="lnr lnr-chevron-right"></span></div>'
  });

  $('.thumbnail-carousel').slick({
    slidesToShow: 3,
    slidesToScroll: 1,
    asNavFor: '.main-carousel',
    dots: false,
    centerMode: false,
    focusOnSelect: true,
    arrows: false
  });
}); 