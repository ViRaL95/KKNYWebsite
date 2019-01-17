$(document).ready(function(){
    $("#sign_up_button").click(function(){
        first_name = $("#first_name_sign_up").val();
        last_name = $("#last_name_sign_up").val();
        gender_is_checked = $("#female_radio").is(":checked") || $("#male_radio").is(":checked");
        email = $("#email_signup").val();
        password = $("#password_signup").val();
        repeat_password = $("#repeat_password_signup").val();
        if (email.trim() == "" || password.trim() == "" || first_name.trim() == "" || last_name.trim() == ""|| repeat_password.trim() == "" || ! gender_is_checked){
            swal({
                title: 'Error!',
                text: 'Missing item',
                type: 'error',
                confirmButtonText: "Okay!"
            })
        }
        else{
             if ($("#female_radio").is(":checked")){
                 gender = "female";
             }
             else{
                 gender = "male";
             }
             sign_up_data = {"first_name": first_name, "last_name": last_name, "gender": gender, "email": email, "password": password, "repeat_password": repeat_password};

             $.ajax({
                type: "POST",
                url: 'sign_up',
                contentType: 'application/json',
                data: JSON.stringify(sign_up_data),
                success: success
            });
            function success(data){
                successful_sign_up = JSON.parse(data);
                if (! successful_sign_up.user_signed_up){
                  swal({
                    title: 'Error!',
                    text: successful_sign_up.message,
                    type: 'error',
                    confirmButtonText: "Okay!"
                  })
                }
                else{
                    window.location.replace("/");
                }
            }
        }
    })
})
