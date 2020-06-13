$(document).ready(function(){

    $("#donation_input_amount").on("input", function(e){
        amt = $(this).val();
        $("#paypal_amount").val(amt);
    })

})
