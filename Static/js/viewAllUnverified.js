window.onload = function (){
	main();
}

function main(){
	console.log("abc")

	$('.verifyLicence').click(function(){
		var id = $(this).parent().parent().attr('id')
		console.log(id)
		window.open("/adminVerification.html/?id=" + id, "_blank")
		// window.location.href = ;
	})

	$('.verifyPan').click(function(){

		var id = $(this).parent().parent().attr('id')
		$.ajax({
			
			type: 'GET',
			url: '/adminVerificationPan',
			data: {

				'id':id
			},
			success:function(data){
			}
		});

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