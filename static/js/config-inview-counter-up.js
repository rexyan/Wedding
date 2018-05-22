'use strict';
$(function() {
  inView('.counter-wrapper')
    .once('enter', function(){
      $.each($('.js-countup'), function () {
        var options = {
          useEasing : true
        };
        var count = $(this).data('count'),
            numAnim = new CountUp(this, 0, count, 0, 5);
        numAnim.start();
      });
    });
  inView.threshold(0.5);
});  