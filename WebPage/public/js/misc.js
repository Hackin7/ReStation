$.ajax({
  url: "header.html",
  success: function(data) {
      $(data).appendTo("header");
  }
});

//Nav bar gets fixed when we scroll pass header
$(function () {
  $(document).scroll(function () {
    var $header = $("header"), $nav = $(".navbar");
    $nav.toggleClass('fixed-top', $(this).scrollTop() > $header.height());
  });
});

function setJumbotronImg(imgName){
	$(document).ready(function(){  
      $(".main-banner").css("background-image", `url(../images/${imgName}.jpg`);
    })
}