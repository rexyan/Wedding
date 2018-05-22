'use strict';
$(function() {
  $('.carousel-product').slick({
    dots: false,
    infinite: false,
    speed: 300,
    arrows: true,
    slidesToShow: 4,
    slidesToScroll: 1,
    nextArrow: '<div class="carousel-arrow prev"><span class="lnr lnr-chevron-left"></span></div>',
    prevArrow: '<div class="carousel-arrow next"><span class="lnr lnr-chevron-right"></span></div>',
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 3,
          slidesToScroll: 1,
          infinite: false,
          dots: false
        }
      },
      {
        breakpoint: 600,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 1
        }
      },
      {
        breakpoint: 480,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1
        }
      }
    ]
  });

  $('.about-carousel').slick({
    dots: false,
    infinite: false,
    speed: 300,
    arrows: true,
    slidesToShow: 3,
    slidesToScroll: 1,
    nextArrow: '<div class="carousel-arrow prev"><span class="lnr lnr-chevron-left"></span></div>',
    prevArrow: '<div class="carousel-arrow next"><span class="lnr lnr-chevron-right"></span></div>',
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 3,
          slidesToScroll: 1,
          infinite: false,
          dots: false
        }
      },
      {
        breakpoint: 600,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 1
        }
      },
      {
        breakpoint: 480,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1
        }
      }
    ]
  });

  $('.carousel-flower').slick({
    dots: false,
    infinite: false,
    speed: 300,
    arrows: true,
    slidesToShow: 1,
    slidesToScroll: 1,
    nextArrow: '<div class="flower-arrow prev"><span class="lnr lnr-chevron-left"></span></div>',
    prevArrow: '<div class="flower-arrow next"><span class="lnr lnr-chevron-right"></span></div>'
  });
});  