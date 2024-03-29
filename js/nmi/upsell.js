var nextpage = "confirm.html";
var storeid = "549e245309d02402762df3a9";
var pid = "549e2b2f09d024031841af29";

function getValue(variable) {
    var query = window.location.search.substring(1);
    var vars = query.split("&");
    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split("=");
        if (pair[0] == variable) {
            return pair[1];
        }
    }
    return "";
}

function create_hidden_input(form_id, name, value) {
    form_id = "#" + form_id;
    form_ob = $(form_id);


    $("<input name='" + name + "' id='" + name + "' type='hidden' value='" + value + "'/>").appendTo(form_ob);
}


function check_cookie(name) {
    if ($.cookie(name) == undefined) {
        rand_num = Math.floor(Math.random() * (max - min)) + min;
        $.cookie(name, rand_num.toString(), {
           expires: 7,
            path: '/'
        });
    }
    return $.cookie(name);
}

var landingpage_id = '1';
var aff_id = checkValue('aff_id');
var c1 = checkValue('c1');
var c2 = checkValue('c2');
var c3 = checkValue('c3');
var c4 = checkValue('c4');
var c5 = checkValue('c5');
var t1 = checkValue('t1');
var uniqid = check_cookie('uniqid');

$('document').ready(function() {
create_hidden_input('orderform', "pid", pid);
create_hidden_input('orderform', "aff_id", aff_id);
create_hidden_input('orderform', "c1", c1);
create_hidden_input('orderform', "c2", c2);
create_hidden_input('orderform', "c3", c3);
create_hidden_input('orderform', "uniqid", uniqid);
create_hidden_input('orderform', "orderpage", window.location.href);
create_hidden_input('orderform', "quantity", 1);
//get_token = get_token()

$("#nothanksbutton").on("click", function() {
$.cookie('upsell', false, { expires: 7, path: '/' });
window.location.href = nextpage;
});


$("#orderform").on("submit", function() {$.ajax({
    url: 'https://'+document.domain+'/api/order/'+storeid+'/'+$.cookie('custid')+'/'+$.cookie('cardid'),
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
});
