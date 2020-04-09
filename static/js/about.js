$(document).ready(function(){
     $("#previous_events_carousel").slick({variableWidth: true, slidesToShow:2, slidesToScroll: 2, dots: true, autoplay: true, autoplaySpeed: 1500});
     $("#translate_origins_to_kannada").click(function(){
     	$("#translate_origins_to_kannada").hide();
        $("#translate_origins_to_english").show();
        $("#kannada_origins_translation").show();
        $("#english_origins_translation").hide();
     })
    $("#translate_origins_to_english").click(function(){
        $("#translate_origins_to_english").hide();
        $("#translate_origins_to_kannada").show();
        $("#english_origins_translation").show();
        $("#kannada_origins_translation").hide();
     })
     $("#view_important_document_button").click(function (){
       selected_document = $("#view_important_document_select").val();
       if (selected_document == "CONSTITUTION"){
           window.open('/static/documents/CONSTITUTION_OF_KKNY.pdf');
       }
       else if (selected_document == "ELECTION_PROCESS"){
           window.open('static/documents/ElectionProcess.pdf');
       }
       else if (selected_document == "MEMBERSHIP_RECOMMENDATIONS"){
           window.open('static/documents/Membership-Recom.pdf');
       }
       else if (selected_document == "GENERAL_BODY_PROCESS"){
           window.open('static/documents/general_body_process.docx');
       }

      })
      $("#view_contributions_document_button").click(function(){
          selected_document = $("#view_contributions_document_select").val();

       if (selected_document == "KODAGU_RELIEF_THANKING_LETTER"){
           window.open('static/documents/Kodagu-Relief-Thanking-Letter.pdf');
       }
       else if (selected_document == "KODAGU_RELIEF_THANKING_LETTER_2"){
           window.open('static/documents/Kodagu relief thanking email.docx');
       }
       else if(selected_document == "KODAGU_RELIEF_DONATION_AMOUNT"){
           window.open('static/documents/Kodagu-Relief-Donation-Amount.pdf');
       }
       else if(selected_document == "KODAGU_RELIEF_DONATION_AMOUNT_2"){
           window.open('static/documents/Kodagu-Relief-Donation-Amount.jpg');
       }
       else if (selected_document == "SEVANJALI_THANKING_LETTER"){
           window.open('static/documents/sevanjali_charitable_trust.jpeg');
       }
      })
     $("#corona_virus_audio_file_button").click(function(){
         window.open('static/audio_files/corona.m4a');

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

