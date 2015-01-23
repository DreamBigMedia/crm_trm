var nextpage = "order.html";
var storeid = "458";
var pid = "12342";
var amount = 4.95;

$('document').ready(function() {

create_hidden_input('orderform', "storeid", storeid);
create_hidden_input('orderform', "pid", pid);
create_hidden_input('orderform', "amount", amount);
create_hidden_input('orderform', "aff_id", aff_id);
create_hidden_input('orderform', "c1", c1);
create_hidden_input('orderform', "c2", c2);
create_hidden_input('orderform', "c3", c3);
create_hidden_input('orderform', "affid", aff_id);
create_hidden_input('orderform', "uniqid", uniqid);
create_hidden_input('orderform', "orderpage", window.location.href);

$("#orderform").on("submit", function() {
$.ajax({
    url: 'https://'+document.domain+'/api/customer',
    data: $("#orderform").serialize(),
    type: 'POST',
    xhrFields: {
        withCredentials: true
    },
    success: function(response) {
        if (response) {
			$.cookie('custid', response, { expires: 7, path: '/' });
                        window.location.href = nextpage;
        }


    },

    error: function(error) {
        console.log(error);
    }
});
return false;
});
});
