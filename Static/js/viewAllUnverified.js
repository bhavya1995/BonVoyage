window.onload = function (){
	main();
}

function main(){
	console.log("abc")
	$('tr').click(function(){
		var id = $(this).attr('id')
		console.log(id)
		window.location.href = "/adminVerification.html/?id=" + id;
	})
}