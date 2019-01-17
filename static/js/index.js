$(document).ready(function(){
    $("#upcoming_events_carousel").slick({variableWidth: true, slidesToShow:2, slidesToScroll: 2, dots: true, autoplay: true, autoplaySpeed: 1500});
    first_name = $("#users_first_name");
    if (first_name.length){
        $.notify("Welcome " + first_name.data().name + "!", {position: "top left"});
    }
})
