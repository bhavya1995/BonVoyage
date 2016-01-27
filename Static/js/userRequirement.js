window.onload = function (){
	main();
}

function main (){
	var owlCarouselCount = 0
	$('.preloader-wrapper').css('display', 'none')

	// $(".owl-carousel").owlCarousel({

	// 	items: 4,
	// 	slideSpeed : 300,
 //    	paginationSpeed : 400,
 //    	navigation : true,
	// });


 $(function () {
         var lat = 40,
             lng = -105,
             latlng = new google.maps.LatLng(lat, lng)
            // image = 'http://www.google.com/intl/en_us/mapfiles/ms/micons/blue-dot.png';

         //zoomControl: true,
         //zoomControlOptions: google.maps.ZoomControlStyle.LARGE,

         var mapOptions = {
             center: new google.maps.LatLng(lat, lng),
             zoom: 4,
             mapTypeId: google.maps.MapTypeId.ROADMAP,
             panControl: true,
             panControlOptions: {
                 position: google.maps.ControlPosition.TOP_RIGHT
             },
             zoomControl: true,
             zoomControlOptions: {
                 style: google.maps.ZoomControlStyle.LARGE,
                 position: google.maps.ControlPosition.TOP_left
             }
         },
         map = new google.maps.Map(document.getElementById('map_canvas'), mapOptions),
             marker = new google.maps.Marker({
                 position: latlng,
                 map: map
              //   icon: image
             });

         var input = document.getElementsByClassName('gllpLocationName');
         var autocomplete = new google.maps.places.Autocomplete(input, {
             types: ["geocode"]
         });

         autocomplete.bindTo('bounds', map);
         var infowindow = new google.maps.InfoWindow();

         google.maps.event.addListener(autocomplete, 'place_changed', function (event) {
             infowindow.close();
             var place = autocomplete.getPlace();
             if (place.geometry.viewport) {
                 map.fitBounds(place.geometry.viewport);
             } else {
                 map.setCenter(place.geometry.location);
                 map.setZoom(17);
             }

             moveMarker(place.name, place.geometry.location);
             $('.gllpLatitude').val(place.geometry.location.lat());
             $('.gllpLongitude').val(place.geometry.location.lng());
         });
         google.maps.event.addListener(map, 'click', function (event) {
             $('.gllpLatitude').val(event.latLng.lat());
             $('.gllpLongitude').val(event.latLng.lng());
             infowindow.close();
                     var geocoder = new google.maps.Geocoder();
                     geocoder.geocode({
                         "latLng":event.latLng
                     }, function (results, status) {
                         console.log(results, status);
                         if (status == google.maps.GeocoderStatus.OK) {
                             console.log(results);
                             var lat = results[0].geometry.location.lat(),
                                 lng = results[0].geometry.location.lng(),
                                 placeName = results[0].address_components[0].long_name,
                                 latlng = new google.maps.LatLng(lat, lng);

                             moveMarker(placeName, latlng);
                             console.log(results[0]);
                             $(".gllpLocationName").val(results[0].formatted_address);
                         }
                     });
         });
        
         function moveMarker(placeName, latlng) {
             //marker.setIcon(image);
             marker.setPosition(latlng);
             infowindow.setContent(placeName);
             //infowindow.open(map, marker);
         }
     });


	$('#addCity').click(function (){
		var city = $('.gllpLocationName').val();
		var div = "<div class='chip brown darken-4 cityName white-text'>" + city + "<i class='material-icons'>close</i></div>";
		$('#cityContainer').append(div);
		$('.gllpLocationName').val("");
		var lat = $('.gllpLatitude').val();
		var lon = $('.gllpLongitude').val();
		var startdate = $('#startDate').val();
		var month = "";
		$('.preloader-wrapper').css('display', 'block')
		if (startdate.toLowerCase().indexOf("january") >= 0){
			month = "01";
		}
		if (startdate.toLowerCase().indexOf("february") >= 0){
			month = "02";
		}
		if (startdate.toLowerCase().indexOf("march") >= 0){
			month = "03";
		}
		if (startdate.toLowerCase().indexOf("april") >= 0){
			month = "04";
		}
		if (startdate.toLowerCase().indexOf("may") >= 0){
			month = "05";
		}
		if (startdate.toLowerCase().indexOf("june") >= 0){
			month = "06";
		}
		if (startdate.toLowerCase().indexOf("july") >= 0){
			month = "07";
		}
		if (startdate.toLowerCase().indexOf("august") >= 0){
			month = "08";
		}
		if (startdate.toLowerCase().indexOf("september") >= 0){
			month = "09";
		}
		if (startdate.toLowerCase().indexOf("october") >= 0){
			month = "10";
		}
		if (startdate.toLowerCase().indexOf("november") >= 0){
			month = "11";
		}
		if (startdate.toLowerCase().indexOf("december") >= 0){
			month = "12";
		}
		console.log(startdate)
		$.ajax({
			type: 'GET',
			url: '/getConditions',
			data: {
				lat: lat,
				lon: lon,
				startDate: month
			},
			success: function (data) {
				console.log(data)
				$('.preloader-wrapper').css('display', 'none')

				classColor = ''
				var divOwl = ''
				var abc = '<div class="owl-carousel-' + owlCarouselCount + ' carousel-container"></div>'
				$('.container-owl-carou-dynamic').append(abc)
				for(var i = 0; i < data.length; i++){
					if(data[i]['verdict'] === 'Fair'){
						classColor = 'orange accent-4'
					}
					if(data[i]['verdict'] === 'Excellent'){
						classColor = 'green darken-4'
					}
					if(data[i]['verdict'] === 'Not Recommended'){
						classColor = 'red darken-4'
					}
					if(data[i]['verdict'] === 'Good'){
						classColor = 'light-green darken-1'
					}
					divOwl += '<div class="card ' + classColor +'">' +
						'<div class="card-content">' +
							'<div class="row card-content-place">' +
								'<p>' + data[i]['placeName'] + '</p>' +
							'</div>' +
							'<div class="row card-content-location">' +
								'<p>' + data[i]['address'] + '</p>' +
							'</div>' + 
							'<div class="row card-content-quality">' +
								'<p>' + data[i]['verdict'] + '</p>' +
							'</div>' + 
						'</div>' +
					'</div>'
				}
				$('.owl-carousel-' + owlCarouselCount).append(divOwl);
				$(".owl-carousel-" + owlCarouselCount).owlCarousel({
					items: 4,
					slideSpeed : 300,
			    	paginationSpeed : 400,
			    	navigation : true,
				});
				owlCarouselCount += 1;
			}
		});
	});

	$('.datepicker').pickadate({
    	selectMonths: true, // Creates a dropdown to control month
    	selectYears: 15 // Creates a dropdown of 15 years to control year
  	});

  	var slider = document.getElementById('noUiSlider');

	noUiSlider.create(slider, {
		start: [0,200000],
		connect: true,
		// margin: 10000,
		step:500,
		range: {
			'min': 0,
			// '2%' : 40000,
			'max': 2000000
		},
		format: wNumb({
			decimals: 0,
			thousand: '',
			prefix: 'Rs.',
		}),
		pips: {
			mode: 'count',
			filter: function(value, type){
				if(value % 500000 == 0){
					return 1;
				}
				return 2;
			},
			// values: [0, 25000, 50000, 200000],
			values: 17,
			density: 10
		}
	});
    var budget = $('#budget');
	slider.noUiSlider.on('update', function( values, handle ) {
		budget.val(values[handle]);
	});

	budget.change(function(){
		slider.noUiSlider.set(this.value);
	})

	$('#submitReq').click(function (){
		var startDate = $('#startDate').val();
		var endDate = $('#endDate').val();
		var budget = $('#budget').val();
		var cities = [];
		$('.cityName').each(function (){
			cities.push(($(this).text()).replace('close', ''));
		})

		$.ajax({
			type: 'GET',
			url: '/submitReq',
			data: {
				startDate: startDate,
				endDate: endDate,
				budget: budget,
				cities: JSON.stringify(cities)
			},
			success: function(data){
				console.log("abc");
				Materialize.toast('Your Requirement has been shared with Travel Agents !', 3000, 'alert-success')
				window.location.href = "/dashboardTraveller"

			}
		});
	});

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