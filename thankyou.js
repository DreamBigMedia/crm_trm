$('document').ready(function() {
if ($.cookie('upsell')=="true") {
	$('.ifnotupsell').hide();
} else {
	$('.ifupsell').hide();
}
$('.orderid').html($.cookie('orderid'));
});
