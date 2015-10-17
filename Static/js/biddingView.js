window.onload=function(){
	main()
}
function main(){
	'use strict';

	$('.modal-trigger').leanModal();

	$('.collapsible').collapsible({
      accordion : false 
    });

	$('.viewPackage').click(function(){

		var id=$(this).attr("id");

		$.ajax({
			type: 'GET',
			url: '/viewAgentPackage',
			data: {
				id:id
			},
			success: function(data){

				$('.viewName').html('');
				$('.viewPackageName').html('');
				$('.viewPrice').html('');
				$('.viewBid').html('');
				$('.viewRemarks').html('');
				$('.airportForm').html('');
				$('.customFormHotel').html('');
				$('.tourGuide').html('');

				if((data['Airports'].length) >0){
					
					$('.airportForm').html('<label class="travellabel">Travel Details</label>');
				}
				if((data['Hotels'].length) >0){

					$('.customFormHotel').html('<label class="travellabel">Hotel Details</label>');
				}
				if((data['Days'].length)){

					$('.tourGuide').html('<label class="travellabel">Tour-Guide Details</label>	');
				}

				$('.viewName').html(data['Name']);
				$('.viewPackageName').html(data['PackageName']);
				$('.viewPrice').html(data['Price']);
				$('.viewBid').html(data['Bid']);
				$('.viewRemarks').html(data['Remarks']);


				for (var i=0;i<(data['Airports'].length);i++){

					var html="<div class='row flightRow'><div class='input-field col s4'><i class='fa fa-plane prefix'></i><label for='airports'>Departure Airport</label><input id='airports' type='text' disabled style='border-bottom:none' class='validate air departure' placeholder='Departure Airport' value='"+data['Airports'][i]["DepartureAirport"]+"'></div><div class='input-field col s4'><i class='fa fa-plane prefix'></i><label for='airports'>Arrival Airport</label><input disabled style='border-bottom:none' id='airports' type='text' class='validate air arrival' placeholder='Arrival Airport' value='"+data['Airports'][i]["ArrivalAirport"]+"'></div><div class='input-field col s4'><label>Seat Type</label><input disabled style='border-bottom:none' id='seatType' type='text' class='validate air seat-type' placeholder='Arrival Airport' value='"+data['Airports'][i]["SeatType"]+"'></div></div>";
					$('.airportForm').append(html);
				}

				for (var i=0;i<(data['Hotels'].length);i++){

					var html="<div class='row hotel-details' id='hotel-row'><div class='input-field col s4'><i class='fa fa-bed prefix'></i><label for='hotel-name'>Hotel Name</label><input disabled style='border-bottom:none' id='hotel-name' type='text' class='validate air' placeholder='Hotel Name' value='"+data['Hotels'][i]["HotelName"]+"'></div><div class='input-field col s3'><i class='fa fa-building prefix'></i><label for='hotel-city'>City</label><input disabled style='border-bottom:none' id='hotel-city' type='text' class='validate air' placeholder='City' value='"+data['Hotels'][i]["HotelCity"]+"'></div><div class='input-field col s2'><label for='room-type'>Room Type</label><input disabled style='border-bottom:none' id='room-type' type='text' class='validate air' placeholder='Room Type' value='"+data['Hotels'][i]["HotelRoomType"]+"'></div><div class='input-field col s3'><label for='num-of-days-nights'>Number of Days and Nights</label><input disabled style='border-bottom:none' id='num-of-days-nights' type='text' class='validate air' placeholder='Number of Days and Nights' value='"+data['Hotels'][i]["HotelNoDays"]+"'></div></div>";
					$('.customFormHotel').append(html);
				}
				
				for (var i=0;i<(data['Days'].length);i++){

					var html="<div class='row tour-guide' id='tour-guide'><div class='input-field col s12'><input disabled style='border-bottom:none;border-bottom: none;padding-left: 2%;font-size: 18px;color: inherit;margin-bottom: 0px;background-color: #FAFAFA;border: 0px;width: inherit' id='day' class='materialize-textarea' value='"+data['Days'][i]["Details"]+"'><label for='day' style='margin-left: 0px !important'>Details For Day '"+data['Days'][i]["index"]+"'</label></div></div>";
					$('.tourGuide').append(html);
				}	
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
