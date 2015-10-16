window.onload=function(){
	main()
}
function main(){
	'use strict';
	$('.signupCustom').click(function(){
		var email = $('#form-email').val()
		$.ajax({
			url: '/login',
			type: 'GET',
			data: {
				'email': email
			},
			success: function(data){
				if ($('#sel1').val() == "Travel-Agent"){
					window.location.href = "/agentVerification.html"
				}
				else{
					window.location.href = "/dashboardTraveller"
				}
			}
		})
	})
	
	$('.login').click(function(){
		var email = $('#form-username').val()
		$.ajax({
			url: '/loginCustom',
			type: 'GET',
			data: {
				'email': email
			},
			success: function(data){
				window.location.href = data['url']
			}
		})
	})

	$('.destinationsButton').click(function(){

		var url="/destinations";
		window.location=url;
	})
}
