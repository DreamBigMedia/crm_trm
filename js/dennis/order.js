var nextpage = "upsell.html";
var storeid = "458";
var pid = "12342";
var amount = 4.95;
var listid = "94f8e5a774c833c477c6c4f577a82ed8"; // Campaign Monitor

$('#orderform').on("load", function() {
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
var m = document.createElement('img'); m.src="https://secure1.m57media.com/clients/p2c/u/pc/?eType=3&cid1="+cid1+"&cid2="+cid2+"&cid3="+cid3+"&cid4="+cid4+"&caid="+caid+"&caCode="+caCode+"&stID="+storeid+"&misc1="+c1+"&misc2="+c2+"&misc3="+c3; m.style.width='1px'; m.style.height='1px'; document.getElementsByTagName('body')[0].appendChild(m);
});

$('document').ready(function() {
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
