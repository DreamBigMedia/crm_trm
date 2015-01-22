$(document).ready(function(){
	//var url = "http://"+ document.domain +":30303/sample/stats/01-01-2010/01-01-2015/me";
	var url;
	
	$('.date').datepicker({
		todayHighlight	: 	true,
		format			:	"dd-mm-yyyy"
	});
	
	$("#show_btn").click(function(){
		
		
		
		$("#stats_table").html("<tr><th></th><th>Clicks</th><th>partials</th><th>Sales</th></tr>");
		$("#stats_table").append("<tr id=\"spinner_row\"><td colspan=\"4\"><div class=\"spinner\"></div></td></tr>");
		
		
		
		var from 	= 	$("#date_from").val();
		var to 		= 	$("#date_to").val();
		
		var year 	= to[6] + to[7] + to[8] + to[9];
		var month 	= to[3] + to[4];
		var day 	= to[0] + to[1];
		
		var date 		= new Date(new Date(year,month-1,day).getTime() + 86400000);
		var new_date 	= (date.getDate() < 10 ? "0" + date.getDate() : date.getDate()) + ((date.getMonth()+1) < 10 ? "-0" + (date.getMonth()+1) : "-" + (date.getMonth()+1)) + "-" + (date.getYear()+1900);
		
		
		url = "http://"+ document.domain +":30303/sample/stats/"+ from +"/"+ new_date +"/me";
		$.post(url, {}, function(data){
			for(var obj in data){
				$("#stats_table").append("<tr><td>"+ obj +"</td><td>"+ data[obj].clicks +"</td><td>"+ data[obj].partials +"</td><td>"+ data[obj].sales +"</td></tr>");
			}
			$("#spinner_row").remove();
		});
		
	});
	
	
	$("#filter_select").on("change", function(){
		
		$("#stats_table").html("<tr><th></th><th>Clicks</th><th>partials</th><th>Sales</th></tr>");
		$("#stats_table").append("<tr id=\"spinner_row\"><td colspan=\"4\"><div class=\"spinner\"></div></td></tr>");
		
		
		var option = $(this).val();
		var from, to;
		if(option == "today"){
			var from_date = new Date().getTime();
			var to_date = new Date(new Date().getTime() + 86400000);
			
			var date = new Date(from_date);
			from 	= (date.getDate() < 10 ? "0" + date.getDate() : date.getDate()) + ((date.getMonth()+1) < 10 ? "-0" + (date.getMonth()+1) : "-" + (date.getMonth()+1)) + "-" + (date.getYear()+1900);
			
			date = new Date(to_date);
			to 	= (date.getDate() < 10 ? "0" + date.getDate() : date.getDate()) + ((date.getMonth()+1) < 10 ? "-0" + (date.getMonth()+1) : "-" + (date.getMonth()+1)) + "-" + (date.getYear()+1900);
		}else if(option == "this_week"){
			var today = new Date();
			var date = new Date(today.getTime() - today.getDay() * 86400000);
			
			from 	= (date.getDate() < 10 ? "0" + date.getDate() : date.getDate()) + ((date.getMonth()+1) < 10 ? "-0" + (date.getMonth()+1) : "-" + (date.getMonth()+1)) + "-" + (date.getYear()+1900);
			
			var to_date = new Date(new Date().getTime() + 86400000);
			date = new Date(to_date);
			to 	= (date.getDate() < 10 ? "0" + date.getDate() : date.getDate()) + ((date.getMonth()+1) < 10 ? "-0" + (date.getMonth()+1) : "-" + (date.getMonth()+1)) + "-" + (date.getYear()+1900);
		}else if(option == "this_month"){
			var today = new Date();
			date = new Date(today.getYear() + 1900, today.getMonth(), 1);
			from 	= (date.getDate() < 10 ? "0" + date.getDate() : date.getDate()) + ((date.getMonth()+1) < 10 ? "-0" + (date.getMonth()+1) : "-" + (date.getMonth()+1)) + "-" + (date.getYear()+1900);
			
			var to_date = new Date(new Date().getTime() + 86400000);
			date = new Date(to_date);
			to 	= (date.getDate() < 10 ? "0" + date.getDate() : date.getDate()) + ((date.getMonth()+1) < 10 ? "-0" + (date.getMonth()+1) : "-" + (date.getMonth()+1)) + "-" + (date.getYear()+1900);
		}else if(option == "three_months"){
			
		}else if(option == "this_year"){
			var date = new Date((new Date().getYear() + 1900), 0, 1);
			from 	= (date.getDate() < 10 ? "0" + date.getDate() : date.getDate()) + ((date.getMonth()+1) < 10 ? "-0" + (date.getMonth()+1) : "-" + (date.getMonth()+1)) + "-" + (date.getYear()+1900);
			
			var to_date = new Date(new Date().getTime() + 86400000);
			date = new Date(to_date);
			to 	= (date.getDate() < 10 ? "0" + date.getDate() : date.getDate()) + ((date.getMonth()+1) < 10 ? "-0" + (date.getMonth()+1) : "-" + (date.getMonth()+1)) + "-" + (date.getYear()+1900);
		}else{}
		
		url = "http://"+ document.domain +":30303/sample/stats/"+ from +"/"+ to +"/me";
		$.post(url, {}, function(data){
			for(var obj in data){
				$("#stats_table").append("<tr><td>"+ obj +"</td><td>"+ data[obj].clicks +"</td><td>"+ data[obj].partials +"</td><td>"+ data[obj].sales +"</td></tr>");
			}
			$("#spinner_row").remove();
		});
		
		
	});
	
	
	
	
});