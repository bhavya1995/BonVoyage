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

	$('.signout').click(function(){

		$.ajax({
			
			type: 'GET',
			url: '/logout',
			success:function(data){

				Materialize.toast('You Have Been Logged Out Successfully!', 4000)
				var url = "/";
				window.location.href=url;
			}
		});
	})

	$('.imageClass').click(function(){

		var url = "/";
		window.location.href=url;
	})
}