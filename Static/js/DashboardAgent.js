window.onload=function(){
	main()
}
function main(){
	'use strict';

	$('.viewBid').click(function(){

		var id=$(this).parent().parent().attr("id");
		var url='/dashboardAgent/bid?q='+id;
		window.location=url;
	})

	$('.addPackage').click(function(){

		var id=$(this).parent().parent().attr("id");
		var url='/makePackage?q='+id;
		window.location=url;
	})
}