window.onload=function(){
	main()
}
function main(){
	'use strict';
	var introguide = introJs();
	introguide.start();
	$('.signupCustom').click(function(){
		var email = $('#form-email').val()
		var password = $('#pass').val()
		var firstName= $('#form-first-name').val()
		var lastName= $('#form-last-name').val()
		var number= $('#form-mobile').val()
		var type=$('#sel1').val()

		$.ajax({
			url: '/login',
			type: 'GET',
			data: {
				'email': email,
				'password':password,
				'firstName':firstName,
				'lastName':lastName,
				'number':number,
				'type':type
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
		var password= $('#form-password').val()
		$.ajax({
			url: '/loginCustom',
			type: 'GET',
			data: {
				'email': email,
				'password':password
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

	$('.tile').hover(function(){

		$('.oddTile').css("background-color","#3A403E");
		$('.evenTile').css("background-color","#1E1E1E");
		$(this).css("background-color","#3E2723");
	})

	$("#postRequirement").click(function(){

		var url="/userRequirement";
		window.location=url;
	})

	$("#postQuotation").click(function(){

		var url="/makePackage";
		window.location=url;
	})

	$("#agentVerification").click(function(){

		var url="/agentVerification.html";
		window.location=url;
	})

	$("#adminVerification").click(function(){

		console.log("In");
		var url="/allAgents.html";
		window.location=url;
	})
}
