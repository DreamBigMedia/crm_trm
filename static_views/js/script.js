$(document).ready(function(){
	//var url = "http://"+ document.domain +":30303/sample/stats/01-01-2010/01-01-2015/me";
	var url;
	
	//url = "http://localhost/hamik/table/data.json";
	
	
	var user;
	
	
	$('.date').datepicker({
		todayHighlight	: 	true,
		format			:	"mm-dd-yyyy"
	});
	
	$("#show_btn").click(function(){
		
		user = $("#username").val();
		//if(user == "") user = "me";
		
		$("#stats_table").html("<tr><th></th><th>Clicks</th><th>partials</th><th>Sales</th><th>Upsales</th></tr>");
		$("#stats_table").append("<tr id=\"spinner_row\"><td colspan=\"4\"><div class=\"spinner\"></div></td></tr>");
		
		
		
		var from 	= 	$("#date_from").val();
		var to 		= 	$("#date_to").val();
		
		from = from[3] + from[4] + "-" + from[0] + from[1] + "-" + from[6] + from[7] + from[8] + from[9];
		to = to[3] + to[4] + "-" + to[0] + to[1] + "-" + to[6] + to[7] + to[8] + to[9];
		
		var year 	= to[6] + to[7] + to[8] + to[9];
		var month 	= to[3] + to[4];
		var day 	= to[0] + to[1];
		
		var date 		= new Date(new Date(year,month-1,day).getTime() + 86400000);
		var new_date 	= (date.getDate() < 10 ? "0" + date.getDate() : date.getDate()) + ((date.getMonth()+1) < 10 ? "-0" + (date.getMonth()+1) : "-" + (date.getMonth()+1)) + "-" + (date.getYear()+1900);
		
		from = $("#date_from").val();
		new_date = new_date[3] + new_date[4] + "-" + new_date[0] + new_date[1] + "-" + new_date[6] + new_date[7] + new_date[8] + new_date[9];
		
		url = "http://"+ document.domain +":30303/stats/daterange/"+ from +"/"+ new_date +"/"+ user;
		$.get(url, {}, function(data){
		
			for (var i in data) {
			  if(data[i].clicks == null) delete data[i];
			}
		
			for(var obj in data){
				$("#stats_table").append("<tr><td>"+ obj +"</td><td>"+ data[obj].clicks +"</td><td>"+ data[obj].partials +"</td><td>"+ data[obj].sales +"</td><td>"+ data[obj].upsales +"</td></tr>");
			}
			$("#spinner_row").remove();
			update_chart(data);
		});
		
	});
	
	
	$("#filter_select").on("change", function(){
		
		$("#stats_table").html("<tr><th></th><th>Clicks</th><th>partials</th><th>Sales</th><th>Upsales</th></tr>");
		$("#stats_table").append("<tr id=\"spinner_row\"><td colspan=\"4\"><div class=\"spinner\"></div></td></tr>");
		
		user = $("#username").val();
		//if(user == "") user = "me";
		
		
		var option = $(this).val();
		var from, to;
		
		if(option == "none"){
			$("#stats_table").html("");
			$("#chartContainer").html("Please Select an Option");
			return;
		}
		
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
		
		
		from = from[3] + from[4] + "-" + from[0] + from[1] + "-" + from[6] + from[7] + from[8] + from[9];
		to = to[3] + to[4] + "-" + to[0] + to[1] + "-" + to[6] + to[7] + to[8] + to[9];
		
		url = "http://"+ document.domain +":30303/stats/daterange/"+ from +"/"+ to +"/"+ user;
		$.get(url, {}, function(data){
			
			for (var i in data) {
			  if(data[i].clicks == null) delete data[i];
			}
			
			for(var obj in data){
				$("#stats_table").append("<tr><td>"+ obj +"</td><td>"+ data[obj].clicks +"</td><td>"+ data[obj].partials +"</td><td>"+ data[obj].sales +"</td><td>"+ data[obj].upsales +"</td></tr>");
			}
			$("#spinner_row").remove();
			update_chart(data);
		});
		
		
	});
	
		function update_chart(data){
			var stats = [];
			
			// Clicks
			var stats_obj = {type: "stackedColumn",name: "Clicks"};
			var stats_obj_data_series = [];
			for(var obj in data){
				stats_obj_data_series.push({y: data[obj].clicks, label: obj});
			}
			stats_obj.dataPoints = stats_obj_data_series;
			stats.push(stats_obj);
			
			// Partials
			stats_obj = {type: "stackedColumn",name: "Partials"};
			stats_obj_data_series = [];
			for(var obj in data){
				stats_obj_data_series.push({y: data[obj].partials, label: obj});
			}
			stats_obj.dataPoints = stats_obj_data_series;
			stats.push(stats_obj);
			
			// Sales
			stats_obj = {type: "stackedColumn",name: "Sales"};
			stats_obj_data_series = [];
			for(var obj in data){
				stats_obj_data_series.push({y: data[obj].sales, label: obj});
			}
			stats_obj.dataPoints = stats_obj_data_series;
			stats.push(stats_obj);
			
			// Upsales
			stats_obj = {type: "stackedColumn",name: "Upsales"};
			stats_obj_data_series = [];
			for(var obj in data){
				stats_obj_data_series.push({y: data[obj].upsales, label: obj});
			}
			stats_obj.dataPoints = stats_obj_data_series;
			stats.push(stats_obj);
			
			
			var chart = new CanvasJS.Chart("chartContainer",
				{
					title:{
						text: ""
					},
					toolTip:{             
						content: function(e){
						  var content;
						  content = e.entries[0].dataSeries.name + " <strong>"+e.entries[0].dataPoint.y  ;
						  return content;
						}
					},
					data: stats
				}
			);
			chart.render();
		}
		

		
	
});

