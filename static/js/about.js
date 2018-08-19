$(document).ready(function(){
     $("#previous_events_carousel").slick({variableWidth: true, slidesToShow:2, slidesToScroll: 2, dots: true, autoplay: true, autoplaySpeed: 1500});
     $("#translate_origins_to_kannada").click(function(){
     	$("#translate_origins_to_kannada").hide();
        $("#translate_origins_to_english").show();
        $("#kannada_origins_translation").show();
        $("#english_origins_translation").hide();
        $("#origins_of_kkny").css("height", "400px");
     })
    $("#translate_origins_to_english").click(function(){
        $("#translate_origins_to_english").hide();
        $("#translate_origins_to_kannada").show();
        $("#english_origins_translation").show();
        $("#kannada_origins_translation").hide();
        $("#origins_of_kkny").css("height", "700px");
     })
     $("#view_document_button").click(function (){
       selected_document = $("#view_document_select").val();
       console.log(selected_document);
       if (selected_document == "CONSTITUTION"){
           window.open('/static/documents/CONSTITUTION_OF_KKNY.pdf');
       }
       else if (selected_document == "ELECTION_PROCESS"){
           window.open('static/documents/ElectionProcess.pdf');
       }
       else if (selected_document == "MEMBERSHIP_RECOMMENDATIONS"){
           window.open('static/documents/Membership-Recom.pdf');
       }


     })
})


function make_request(email, name, content){
    data = {
        "email": email,
        "name": name,
        "content": content,
    }   

    request = {
        type: 'POST',
        url: 'sendSuggestionToSuggestionsBox',
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: success,
        error: error
    }

    function success(){
        $("#warning").html("Your email will be sent to KKNY's suggestion box");
    }
    
    function error(){
        $("#warning").html("<h3 style='color: red'> Something went wrong, please contact an administrator </h3>");
    }

    $.ajax(request);
}

