window.onload = function (){
	main()
}

function main (){
	$('#pre-loader').css('display', 'none');
	$('.start').click(function(){
		console.log("abc")
		$('#pre-loader').css('display', 'block');

		var progress = setInterval(function () {
		    var $bar = $('.bar');

		    if ($bar.width() >= 400) {
		        clearInterval(progress);
		        $('.progress').removeClass('active');
		    } else {
		        $bar.width($bar.width() + 40);
		    }
		    $bar.text("Please wait while we use Image Processing !");
		}, 800);


		$.ajax({
			url: '/imageProcessing',
			type: 'GET',
			data: {
  				'imageName': $($('table tr td a')[0]).prop('title'),
			},
			success: function(data){
				console.log("adad")
				console.log(data)
				$('#licenceNum').val(data['licenceNum'])
				$('#name').val(data['name'])
				$('#fathersName').val(data['fathersName'])
				$('#address').val(data['address'])
				$('#dobInput').val(data['dob'])
				$('#pre-loader').css('display', 'none');

			}
		})

		$.ajax({
			url: '/imageProcessingPan',
			type: 'GET',
			data: {
  				'imageName': $($('table tr td a')[2]).prop('title')
			},
			success: function(data){
				console.log("adad")
				console.log(data)
				$('#PanCardNo').val(data['panNum'])
				$('#namePan').val(data['name'])
				$('#fathersNamePan').val(data['fathersName'])
				$('#dobInputPan').val(data['dob'])
				$('#pre-loader').css('display', 'none');

			}
		})

	})


	$('#submitReq').click(function(){
		var licenceNum = $('#licenceNum').val()
		var name = $('#name').val()
		var fathersName = $('#fathersName').val()
		var address = $('#address').val()
		var dob = $('#dobInput').val()
		var panNum = $('#PanCardNo').val()
		var namePan = $('#namePan').val()
		var fathersNamePan = $('#fathersNamePan').val()
		var dobPan = $('#dobInputPan').val()
		$.ajax({
			url: '/submitAgentDetails',
			type: 'GET',
			data: {
				'licenceNum': licenceNum,
				'name': name,
				'fathersName': fathersName,
				'address': address,
				'dob': dob,
				'panNum': panNum,
				'namePan': namePan,
				'fathersNamePan': fathersNamePan,
				'dobPan': dobPan
			},
			success: function(data){
				window.location.href = "/dashboardAgent"
			}
		});

	});
}