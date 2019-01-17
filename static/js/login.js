$(document).ready(function(){
    $("#login_button").click(function(){
        email = $("#email_login").val();
        password = $("#password_login").val();
        if (email.trim() == "" || password.trim() == ""){
            swal({
                title: 'Error!',
                text: 'Missing item',
                type: 'error',
                confirmButtonText: "Okay!"
            })
        }
        else{
            login_data = {"email": email, "password": password};
            console.log(login_data);
            $.ajax({
                type: "POST",
                url: 'login',
                contentType: 'application/json',
                data: JSON.stringify(login_data),
                success: success
            });
            function success(verify_user){
               user_information = JSON.parse(verify_user);
               if (! user_information.user_exists){
    	           swal({
                     title: 'Error!',
                     text: 'Wrong username/password combination',
                     type: 'error',
                     confirmButtonText: "Okay!"
                  })
               }
               else{
                   if(user_information.hasOwnProperty("redirect_to")){
                       window.location.replace(user_information.redirect_to);
		   }
  		   else{
                       window.location.replace("/");
                   }
               }
            }
        }
    })
})
