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
        rand_num = Math.floor(Math.random() * (999999 - 100000)) + 100000;
        $.cookie(name, rand_num, {
           expires: 7,
            path: '/'
        });
    }
    return $.cookie(name);
}

var landingpage_id = '1';
var aff_id = checkValue('aff_id');
var caCode = checkValue('caCode');
var caid = checkValue('caid');
var c1 = checkValue('c1');
var c2 = checkValue('c2');
var c3 = checkValue('c3');
var c4 = checkValue('c4');
var c5 = checkValue('c5');
var cid1 = checkValue('cid1');
var cid2 = checkValue('cid2');
var cid3 = checkValue('cid3');
var cid4 = checkValue('cid4');
var cid5 = checkValue('cid5');
var t1 = checkValue('t1');
var uniqid = check_cookie('uniqid');
var dbg_track = "not engaged"

//get_token = get_token()

$.ajax({
    url: 'https://'+document.domain+'/track/',
    data: {
        'c1': c1,
        'c2': c3,
        'c4': c4,
        'c5': c5,
        't1': t1,
	'uniqid': uniqid,
	'affid':aff_id
    },
    type: 'GET',
    xhrFields: {
        withCredentials: true
    },
    success: function(response) {
        if (response) {
            var track_id = response;
            setTimeout(function() {
                $.ajax({
                    url: 'https://'+document.domain+'/engage/' + track_id,
                    xhrFields: {
                        withCredentials: true
                    },
                    type: 'GET',
                    success: function(response) {
                        dbg_track = response;
                        console.log("enaged tracked");
                    }
                });
            }, 13000);
        }


    },

    error: function(error) {
        console.log(error);
    }
});
