'use strict';
$(function() {
  var actionAddToCart = $('.js-action-add-cart');
  var cart = $('.js-widget-shop-cart');
  var itemWishList = $('.js-notify-add-wish-list');

  actionAddToCart.each(function() {
    $(this).on('click', function(e) { 
      var productName = $(this).closest('.product').find('.product-name').text();
      e.preventDefault();
      notifyAddToCart(productName);
      $(this).addClass('is-added');
      setTimeout(function(){
        updateCart();
        actionAddToCart.removeClass('is-added');
      }, 1000);
    }); 
  }); 

  itemWishList.on("click", function(e) {
    e.preventDefault();
    $(this).toggleClass('active');
    var productName = $(this).closest('.product').find('.product-name').text();
    if($(this).hasClass('active')) {
      addToWishList(productName);
    } else {
      removeFromWishList(productName);
    }
  });

  function updateCart() {
    //show counter if this is the first item added to the cart
    ( !cart.hasClass('items-added') ) && cart.addClass('items-added'); 
    var cartItems = cart.find('.counter'),
        text = parseInt(cartItems.text()) + 1;
        cartItems.text(text);
  };

  function notifyAddToCart(productName) {
    $.notify({
      title: productName,
      icon: 'lnr lnr-cart',
      message: "已加入购物车"
    },{
      type: 'success',
      animate: {
        enter: 'animated fadeInUp',
        exit: 'animated fadeOut'
      },
      placement: {
        from: "bottom",
        align: "right"
      },
      offset: 20,
      spacing: 10,
      z_index: 1031,
    });
  };

  function addToWishList(productName) {
    $.notify({
      title: productName,
      icon: 'lnr lnr-heart',
      message: "已收藏"
    },{
      type: 'success',
      animate: {
        enter: 'animated fadeInUp',
        exit: 'animated fadeOut'
      },
      placement: {
        from: "bottom",
        align: "right"
      },
      offset: 20,
      spacing: 10,
      z_index: 1031
    });
  };

  function removeFromWishList(productName) {
    $.notify({
      title: productName,
      icon: 'lnr lnr-heart',
      message: "is removed from wish list"
    },{
      type: 'danger',
      animate: {
        enter: 'animated fadeInUp',
        exit: 'animated fadeOut'
      },
      placement: {
        from: "bottom",
        align: "right"
      },
      offset: 20,
      spacing: 10,
      z_index: 1031,
    });
  };


});