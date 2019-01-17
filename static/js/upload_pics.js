
$(document).ready(function(){
    $("#choose_event").change(function(){
        if ($(this).val() == "Other"){
            $("#upload_image_other_event_name").show();
        }
        else{
            $("#upload_image_other_event_name").hide();
        }
    })
    $("#upload_photo_type_button").click(function(){
      if ( $("#choose_upload_image").get(0).files.length == 0){
        swal({
            title: 'Error!',
            text: 'Missing image(s)',
            type: 'error',
            confirmButtonText: "I'll fix it!"

        })
        return;
      }
      else if ( $("#choose_event").val() == "Other" && $.trim($("#upload_image_other_event_name").val()) == ""){
        swal({
            title: 'Error!',
            text: 'Enter Event Name',
            type: 'error',
            confirmButtonText: "I'll fix it!"
      })
      }
      else{
          var formData = new FormData($("#upload_pics_form")[0]);
          $.ajax({
              url: '/upload_pics/' + $("#choose_event").val(),
              type: 'POST',
              data: formData,
              cache: false,
              contentType: false,
              processData: false,
              error: function(data){
		swal({
		    title: 'Error!',
		    text: 'Something went wrong, contact the developer of this website',
		    type: 'error',
		    confirmButtonText: "Okay!"
		})
                $(".loader").hide();
              },
              success: function (data){
                  $(".loader").hide();
                  if (JSON.parse(data).success){
		      swal(
			 'Successful Upload',
			  JSON.parse(data).message,
			 'success'
		      )
                  }
                  else{
                      swal({
                          title: 'Error!',
                          text: JSON.parse(data).message,
                          type: 'error',
                          confirmButtonText: "Okay!"
                      })

                  }
           },
           statusCode: {
              413: function(data){
                  $(".loader").hide();
                  swal({
                      title: 'Error!',
                      text: retrieveMaxContentLengthErrorMessage(data), 
                      type: 'error',
                      confirmButtonText: 'Okay!'
                  })
              }
           }
       })
       $(".loader").show();
    }
   })
   function retrieveMaxContentLengthErrorMessage(data){
       try{
           return JSON.parse(data.responseText).message;
       }
       catch{
           return "Please do not submit more than 25 MB of data";
       }
   } 
  })
