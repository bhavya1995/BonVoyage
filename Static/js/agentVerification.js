window.onload = function (){
	main()
}

function main (){
	
	$('.start').click(function(){
		console.log("abc")
		$.ajax({
			url: '/imageProcessing',
			type: 'GET',
			data: {
  				'imageName': $($('table tr td a')[0]).prop('title')
			},
			success: function(data){
				console.log("adad")
				console.log(data)
				$('#licenceNum').val(data['licenceNum'])
				$('#name').val(data['name'])
				$('#fathersName').val(data['fathersName'])
				$('#address').val(data['address'])
				$('#dobInput').val(data['dob'])
			}
		})
	})

	$('#submitReq').click(function(){
		var licenceNum = $('#licenceNum').val()
		var name = $('#name').val()
		var fathersName = $('#fathersName').val()
		var address = $('#address').val()
		var dob = $('#dobInput').val()
		$.ajax({
			url: '/submitAgentDetails',
			type: 'GET',
			data: {
				'licenceNum': licenceNum,
				'name': name,
				'fathersName': fathersName,
				'address': address,
				'dob': dob
			},
			success: function(data){
				window.location.href = "/dashboardAgent"
			}
		});

	});
}