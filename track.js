

function getValue(variable)
{
       var query = window.location.search.substring(1);
       var vars = query.split("&");
       for (var i=0;i<vars.length;i++) {
               var pair = vars[i].split("=");
               if(pair[0] == variable){return pair[1];}
       }
       return "";
}

function create_hidden_input(form_id,name,value)
{
  form_id = "#"+form_id;
  form_ob = $(form_id);


  $("<input name='"+name+"' id='"+name+"' type='hidden' value='"+value+"'/>").appendTo(form_ob);
}

function randNumber(min, max) {
  return Math.floor(Math.random() * (max - min)) + min;
}

function get_token()
{
_csrf_token = document.getElementById('_csrf_token').value;
if (_csrf_token !== null && _csrf_token.value === "")
    {

    return _csrf_token;
    }

}

var landingpage_id = '1';
var aff_id = getValue('aff_id');
var c1 = var_aff_id;
var c2 = getValue('c2');
var c3 = getValue('c3');
var c4 = getValue('c4');
var c5 = getValue('c5');
var t1 = getValue('t1');
rand_num = randNumber();
get_token = get_token();
$.ajax({
    url: '/track/',
    data: {'c1':c1,'c2':c3,'c4':c4,'c5':c5,'t1':'t1','l1':rand_num, '_csrf_token':get_token},
    type: 'POST',
    success: function(response) {
        console.log(response);
    },
    error: function(error) {
        console.log(error);
    }
});


