var slider = new Slider(".js-filter-price");
slider.on("slide", function(sliderValue) {
  document.getElementById("js-filter-result-val").textContent = sliderValue;
});