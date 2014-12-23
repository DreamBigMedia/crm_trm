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


function check_cookie(name)
{
       if($.cookie(name)==undefined)
       {
              rand_num = Math.floor(Math.random() * (max - min)) + min;
              $.cookie(name,rand_num, { expires: 7, path: '/' });
       }
       return $.cookie(name);
}

var landingpage_id = '1';
var aff_id = getValue('aff_id');
var c1 = var_aff_id;
var c2 = getValue('c2');
var c3 = getValue('c3');
var c4 = getValue('c4');
var c5 = getValue('c5');
var t1 = getValue('t1');
var uniqid = check_cookie('uniqid');

//get_token = get_token()

$.ajax({
    url: 'http://162.218.236.81:55555/track/',
    data: {'c1':c1,'c2':c3,'c4':c4,'c5':c5,'t1':'t1','l1':l1},
    type: 'POST',
    xhrFields: {
   withCredentials: true
},
    success: function(response) {
           if(response)
        {
               var track_id = response;
               setTimeout(function(){
                      $.ajax({
                            url:'http://162.218.236.81:55555/engage/'+track_id,
                            xhrFields: {
   withCredentials: true
},
                            type : 'GET',
                            success:function(response){
                                   console.log("enaged tracked");}),
}),13000);
               }
                              
              
       },

    error: function(error) {
        console.log(error);
    }
});

