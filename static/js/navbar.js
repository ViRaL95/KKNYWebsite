$(document).ready(function(){
    $("#control_panel span").mouseover(function(){
        $(this).children(".en_translation").hide("slow");
        $(this).children(".kn_translation").show("slow");
    }); 
    $("#control_panel span").mouseleave(function(){
        $(this).children(".kn_translation").hide("slow");
        $(this).children(".en_translation").show("slow");
    })  
})
