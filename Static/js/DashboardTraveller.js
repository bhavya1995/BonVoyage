window.onload=function(){
	main()
}
function main(){
	'use strict';

	$('.rowcount').click(function(){

		var text=$(this).text();
		if(parseInt(text) == 0 ){

			var toastContent = 'You Have No Packages So Far!!! Please Be Patient or Select Packages';
  			Materialize.toast(toastContent, 2000);
		}
		else{

			var id=$(this).parent().parent().attr("id");
			var url='/dashboardTraveller/bid?q='+id;
			window.location=url;	
		}
	});

	$('.selectPackage').click(function(){

		var id=$(this).parent().parent().attr("id");
		var url='/dashboardTraveller/select?q='+id;
		window.location=url;	
	})
	

	$('.shareExperience').click(function(){

		var id=$(this).parent().parent().attr("id");
		var url='/feedback?q='+id;
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