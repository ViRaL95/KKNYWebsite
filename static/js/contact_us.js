$(document).ready(function(){
     $("#contact_button").click(function(){
        var emailregex = /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/;
        var nameregex = /^([A-Z a-z])+$/;
        if(emailregex.test($("#email").val())){
            $("#warning").empty();
        }
        else{
            $("#warning").html("<h3 style='color:red'> Ensure that you entered the correct email</h3>");
            return;
        }
        if(nameregex.test($("#name").val())){
            $("#warning").empty();
        }
        else{
             $("#warning").html("<h3 style='color:red'> Ensure that you entered the correct name</h3>");
            return;
        }
        if($("#suggestion").val().trim() == ""){
             $("#warning").html("<h3 style='color:red'> Ensure that you entered a suggestion</h3>");
            return;
        }
        else{
            $("#warning").empty();
        }
        make_request($("#email").val(), $("#name").val(), $("#suggestion").val());
    })
})
