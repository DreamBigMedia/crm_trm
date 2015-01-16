$(document).ready(function(){
	// http://162.218.236.81:30303/get/affid/me
	$.get("http://162.218.236.81:30303/get/affid/me", {}, function(data){
		
		/*
		*	for products chart
		*/
		var products_data_points = [];
		var products_obj = data;
		for(var obj in products_obj.products){
			var product_ob = {label:products_obj.products[obj].name,y:products_obj.products[obj].sales};
			products_data_points.push(product_ob);
		}
		var products_chart = new CanvasJS.Chart("products_chart");
		products_chart.options.title = {text:""};
		var products_series = {type:"column",name:"products"};
		products_chart.options.data = [];
		products_chart.options.data.push(products_series);
		products_series.dataPoints = products_data_points;
		products_chart.render();

		/*
		*	for engage visitors chart
		*/
		var engage_visitors_data_points = [];
		var ev_obj = data;
		engage_visitors_data_points.push({label:"bought",y:ev_obj.visitors.engage.bought});
		engage_visitors_data_points.push({label:"not bought",y:ev_obj.visitors.engage.notbought});
		var ev_chart = new CanvasJS.Chart("engage_visitors_chart");
		ev_chart.options.title = {text:""};
		var ev_series = {type:"column",name:"engage_visitors"};
		ev_chart.options.data = [];
		ev_chart.options.data.push(ev_series);
		ev_series.dataPoints = engage_visitors_data_points;
		ev_chart.render();
		
		/*
		*	for not engage visitors chart
		*/
		var not_engage_visitors_data_points = [];
		var nev_obj = data;
		not_engage_visitors_data_points.push({label:"bought",y:nev_obj.visitors.notengage.bought});
		not_engage_visitors_data_points.push({label:"not bought",y:nev_obj.visitors.notengage.notbought});
		var nev_chart = new CanvasJS.Chart("not_engage_visitors_chart");
		nev_chart.options.title = {text:""};
		var nev_series = {type:"column",name:"not_engage_visitors"};
		nev_chart.options.data = [];
		nev_chart.options.data.push(nev_series);
		nev_series.dataPoints = not_engage_visitors_data_points;
		nev_chart.render();
		
		$("#sales_chart").on("change", function(){
			var products_chart = new CanvasJS.Chart("products_chart");
			products_chart.options.title = {text:""};
			var products_series = {type:this.value,name:"products"};
			products_chart.options.data = [];
			products_chart.options.data.push(products_series);
			products_series.dataPoints = products_data_points;
			products_chart.render();
		});
		
		$("#engage_visitors_chart_select").on("change", function(){
			var engage_visitors_data_points = [];
			var ev_obj = data;
			engage_visitors_data_points.push({label:"bought",y:ev_obj.visitors.engage.bought});
			engage_visitors_data_points.push({label:"not bought",y:ev_obj.visitors.engage.notbought});
			var ev_chart = new CanvasJS.Chart("engage_visitors_chart");
			ev_chart.options.title = {text:""};
			var ev_series = {type:this.value,name:"engage_visitors"};
			ev_chart.options.data = [];
			ev_chart.options.data.push(ev_series);
			ev_series.dataPoints = engage_visitors_data_points;
			ev_chart.render();
		});
		
		$("#not_engage_visitors_chart_select").on("change", function(){
			var not_engage_visitors_data_points = [];
			var nev_obj = data;
			not_engage_visitors_data_points.push({label:"bought",y:nev_obj.visitors.notengage.bought});
			not_engage_visitors_data_points.push({label:"not bought",y:nev_obj.visitors.notengage.notbought});
			var nev_chart = new CanvasJS.Chart("not_engage_visitors_chart");
			nev_chart.options.title = {text:""};
			var nev_series = {type:this.value,name:"not_engage_visitors"};
			nev_chart.options.data = [];
			nev_chart.options.data.push(nev_series);
			nev_series.dataPoints = not_engage_visitors_data_points;
			nev_chart.render();
		});
		
		$(".canvasjs-chart-credit").css("display","none");
		$("select").on("change", function(){
			$(".canvasjs-chart-credit").css("display","none");
		});
		
		
	});
});


