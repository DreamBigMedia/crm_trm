var nextpage = "order.html";
var storeid = "458";
var pid = "12342";
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
create_hidden_input('orderform', "uniqid", uniqid);
create_hidden_input('orderform', "orderpage", window.location.href);
var m = document.createElement('img'); m.src="https://secure1.m57media.com/clients/p2c/u/pc/?eType=2&cid1="+cid1+"&cid2="+cid2+"&cid3="+cid3+"&cid4="+cid4+"&caid="+caid+"&caCode="+caCode+"&stID="+storeid+"&misc1="+c1+"&misc2="+c2+"&misc3="+c3; m.style.width='1px'; m.style.height='1px'; document.getElementsByTagName('body')[0].appendChild(m);

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
