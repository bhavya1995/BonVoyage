document.ready = function (){
	main();
}

function main(){
	'use strict';

	var counter = 1;
	$('#addAirport').click(function (){
		var div = '<div class="row flightRow"><div class="input-field col s4"><i class="fa fa-plane prefix"></i><label for="airports">Departure Airport</label><input id="airports" type="text" class="validate air departure" placeholder="Departure Airport"></div><div class="input-field col s4"><i class="fa fa-plane prefix"></i><label for="airports">Arrival Airport</label><input id="airports" type="text" class="validate air arrival" placeholder="Arrival Airport"></div><div class="input-field col s4"><select id="seatTypeSelect"><option value="" disabled selected>Seat Type</option><option value="Economic">Economic</option><option value="Business">Business</option><option value="First Class">First Class</option></select><label>Seat Type</label></div></div>';
		$('.customForm').append(div);
	    $('select').material_select();

	    $('.air').keyup(function(){
	    	var element = this;
			$.ajax({
				type: 'GET',
				url: '/getAirports/',
				data:{
					q: $(element).val()
				},
				success: function(data){
				    $( ".air" ).autocomplete({
				      source: data.data.airport
				    });
				}
			})
	    });
	});


	$('#addHotel').click(function() {
		var div1 = '      <div class="row hotel-details" id="hotel-row">'+
		'<div class="input-field col s4">'+
			'<i class="fa fa-bed prefix"></i>'+
			'<label for="hotel-name">Hotel Name</label>'+
			'<input id="hotel-name" type="text" class="validate" placeholder="Hotel Name">'+
		'</div>'+
		'<div class="input-field col s3">'+
		'	<i class="fa fa-building prefix"></i>'+
		'		<label for="hotel-city">City</label>'+
			'<input id="hotel-city" type="text" class="validate" placeholder="City">'+
		'</div>'+
		'<div class="input-field col s2">'+
			'<label for="room-type">Room Type</label>'+
			'<input id="room-type" type="text" class="validate" placeholder="Room Type">'+
		'</div>'+
 		'<div class="input-field col s3">'+
			'<label for="num-of-days-nights">Number of Days and Nights</label>'+
			'<input id="num-of-days-nights" type="text" class="validate" placeholder="Number of Days and Nights">'+
		'</div>'+
 	 '</div>'
		$('.customFormHotel').append(div1)
	});


	$('#addDay').click(function(){
		 counter += 1;
		 var div2 = '<div class="row tour-guide" id="tour-guide">'+
		'<div class="input-field col s12">'+
			'<textarea id="day" class="materialize-textarea"></textarea>'+
          	'<label for="day">Details For Day '+ counter+'</label>'+
  		'</div>'+
 	 '</div>'
 	 $('.tourGuide').append(div2);

	});


	$('#submitReq').click(function(){

		var travelReqId= $(this).parent().attr("id");
		console.log(travelReqId)
		var packageName = $('#packageName').val();
		var packagePrice = $('#price').val();
		var flightDetails = [];
		var hotelDetails = [];
		var tourGuide = [];
		
		$('.flightRow').each(function(){
			var temp = {
				departure: $($(this).find('.departure')).val(),
				arrival: $($(this).find('.arrival')).val(),
				type: $($(this).find('#seatTypeSelect')).val()			
			}
			flightDetails.push(temp);
		});
		
		$('.hotel-details').each(function(){
			var temp = {
				hotelName: $($(this).find('#hotel-name')).val(),
				hotelCity: $($(this).find('#hotel-city')).val(),
				roomType: $($(this).find('#room-type')).val(),
				numOfDaysNights: $($(this).find('#num-of-days-nights')).val()
			}
			hotelDetails.push(temp);
		});
		var day = 1;
		$('.tour-guide').each(function(){
			var temp = {
				day: day,
				description: $($(this).find('#day')).val()
			}
			tourGuide.push(temp);
			day += 1;
		});

		$.ajax({
			type: 'GET',
			url: '/submitPackage',
			data: {

				travelReqId: travelReqId,
				packageName: packageName,
				packagePrice: packagePrice,
				flightDetails: JSON.stringify(flightDetails),
				hotelDetails: JSON.stringify(hotelDetails),
				tourGuide: JSON.stringify(tourGuide)
			},
			success: function(data){
				Materialize.toast('Your Package has been shared with Customer !', 3000, 'alert-success')
				window.location.href = '/dashboardAgent'
			}
		});

	});


    $('.air').keyup(function(){
    	var element = this;
		$.ajax({
			type: 'GET',
			url: '/getAirports/',
			data:{
				q: $(element).val()
			},
			success: function(data){
			    $( ".air" ).autocomplete({
			      source: data.data.airport
			    });
			}
		})
    });
    $('select').material_select();
}
