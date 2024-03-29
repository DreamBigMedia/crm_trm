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
        rand_num = Math.floor(Math.random() * (999999 - 100000)) + 100000;
        $.cookie(name, rand_num, {
           expires: 7,
            path: '/'
        });
    }
    return $.cookie(name);
}

var landingpage_id = '1';
var c1 = getValue('aff_id');
var c2 = getValue('c2');
var c3 = getValue('c3');
var c4 = getValue('c4');
var c5 = getValue('c5');
var t1 = getValue('t1');
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
	'uniqid': uniqid
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
