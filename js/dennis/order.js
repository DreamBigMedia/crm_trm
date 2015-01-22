var nextpage = "upsell.html";
var storeid = "458";
var pid = "12342";
var amount = 4.95;
var listid = "94f8e5a774c833c477c6c4f577a82ed8"; // Campaign Monitor

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

function checkValue(variable) {
    if ($.cookie(variable) == undefined) {
        $.cookie(variable, getValue(variable), {
           expires: 7,
            path: '/'
        });
    }
    return $.cookie(variable);
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

var processing_card = false;
var landingpage_id = '1';
var aff_id = checkValue('aff_id');
var caCode = checkValue('caCode');
var caid = checkValue('caid');
var c1 = checkValue('c1');
var c2 = checkValue('c2');
var c3 = checkValue('c3');
var c4 = checkValue('c4');
var c5 = checkValue('c5');
var t1 = checkValue('t1');
var uniqid = check_cookie('uniqid');

$('document').ready(function() {
create_hidden_input('orderform', "storeid", storeid);
create_hidden_input('orderform', "pid", pid);
create_hidden_input('orderform', "amount", amount);
create_hidden_input('orderform', "c1", c1);
create_hidden_input('orderform', "c2", c2);
create_hidden_input('orderform', "c3", c3);
create_hidden_input('orderform', "affid",aff_id);
create_hidden_input('orderform', "cacode", caCode);
create_hidden_input('orderform', "uniqid", uniqid);
create_hidden_input('orderform', "orderpage", window.location.href);
//get_token = get_token()

$(window).bind('beforeunload', function() {
if ($.cookie('orderid') == undefined) {
$.ajax({
    url: 'https://'+document.domain+'/api/listme/'+listid+'/'+$.cookie('custid'),
    type: 'GET',
    xhrFields: {
        withCredentials: true
    },
    success: function(response) { console.log(response);
    },

    error: function(error) {
        console.log(error);
    }
});
}
});

$("#orderform").on("submit", function() {
$("input[type=image]").attr('disabled', true);
processing_card=true;
$.ajax({
    url: 'https://'+document.domain+'/api/orderWithCard/ucrm/'+$.cookie('custid'),
    data: $("#orderform").serialize(),
    type: 'POST',
    xhrFields: {
        withCredentials: true
    },
    success: function(response) { console.log(response);
        if (response.success) {
			$.cookie('cardid', response.card, { expires: 7, path: '/' });
			$.cookie('orderid', response.order, { expires: 7, path: '/' });
                        window.location.href = nextpage;
        } else {
		alert(decodeURIComponent(response.cc_response).replace("+", " "));
		$("input[type=image]").attr('disabled', false);
	}
    },

    error: function(error) {
        console.log(error);
    }
});
return false;
});
});
