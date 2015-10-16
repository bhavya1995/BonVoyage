window.onload=function(){
	main()
}
function main(){
	'use strict';

	$('.modal-trigger').leanModal();

	$('.collapsible').collapsible({
      accordion : false 
    });

    var slider = document.getElementById('noUiSlider');

	noUiSlider.create(slider, {
		start: [0,500],
		connect: true,
		step: 100,
		range: {
			'min': 0,
			'max': 50000
		},
		format: wNumb({
			decimals: 0,
			thousand: ',',
			postfix: '',
		})
	});

	var budget = $('.bidvalue');
	slider.noUiSlider.on('update', function( values, handle ) {
		budget.val(values[handle]);
	});

	budget.change(function(){
		slider.noUiSlider.set(this.value);
	});

	$('#bid').click(function(){

		var value=$('.bidvalue').val();
		var element=$('.panel_price_righttop').find('a');
		var id=$(element).attr("id");
		
		$.ajax({
			type: 'GET',
			url: '/submitBid',
			data: {
				value:value,
				id:id
			},
			success: function(data){
				Materialize.toast('Bid Added', 4000)
			}
		});
	});

	$('.modal-placeBid').click(function(){

		var element=$('.panel_price_righttop').find('a');
		var id=$(element).attr("id");

		$.ajax({
			type: 'GET',
			url: '/getPackageDetails',
			data: {
				id:id
			},
			success: function(data){
			
				var price=data['Price'];
				var bid=data['Bid'];
				$('#currrentPrice').val(price);
				if(bid=0){

					$('#currrentbid').val(0);	
				}
				$('#currrentbid').val(bid);
			}
		});
	})

	$('.viewPackage').click(function(){

		var id=$(this).attr("id");

		$.ajax({
			type: 'GET',
			url: '/viewPackage',
			data: {
				id:id
			},
			success: function(data){
			
				$('.viewName').html(data['agentName']);
				$('.viewPackageName').html(data['agentPackageName']);
				$('.viewPrice').html(data['agentPrice']);
				$('.viewBid').html(data['agentBid']);
				$('.viewRemarks').html(data['agentRemarks']);
			}
		});
	})
}
