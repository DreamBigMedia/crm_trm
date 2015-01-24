var nextpage = "confirm.html";
var storeid = "458";
var pid = "12343";
var amount = 4.95;

function create_hidden_input(form_id,name,value){form_id="#"+form_id;form_ob=$(form_id);$("<input name='"+name+"' id='"+name+"' type='hidden' value='"+value+"'/>").appendTo(form_ob)}

$('document').ready(function() {
create_hidden_input('orderform', "storeid", storeid);
create_hidden_input('orderform', "pid", pid);
create_hidden_input('orderform', "amount", amount);
create_hidden_input('orderform', "c1", c1);
create_hidden_input('orderform', "c2", c2);
create_hidden_input('orderform', "c3", c3);
create_hidden_input('orderform', "affid", aff_id);
create_hidden_input('orderform', "cacode", caCode);
create_hidden_input('orderform', "uniqid", uniqid);
create_hidden_input('orderform', "orderpage", window.location.href);
//get_token = get_token()
});

$("#nothanksbutton").on("click", function() {
$.cookie('upsell', false, { expires: 7, path: '/' });
window.location.href = nextpage;
});


$("#orderform").on("submit", function() {
$.ajax({
    url: 'https://'+document.domain+'/api/order/ucrm/'+$.cookie('custid')+'/'+$.cookie('cardid'),
    data: $("#orderform").serialize(),
    type: 'POST',
    xhrFields: {
        withCredentials: true
    },
    success: function(response) {
        if (response.success) {
			$.cookie('upsell', true, { expires: 7, path: '/' });
                        window.location.href = nextpage;
        }


    },

    error: function(error) {
        console.log(error);
    }
});
return false;
});
