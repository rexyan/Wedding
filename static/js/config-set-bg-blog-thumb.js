'use strict';
$( document ).ready(function() {
  $('.js-set-bg-blog-thumb').each(function(){
    var imagesURLs = $(this).find('img').attr('src');
    $(this).css('background-image', 'url('+ imagesURLs + ')');
  })
});