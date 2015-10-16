window.onload = function (){
	main ()
}

function main(){
	$('.accept').click(function(){
		var id = $('.first').attr('id')
		$.ajax({
			type: 'GET',
			url: '/approve',
			data: {
				'id': id
			},
			success: function(data){
				window.location.href = '/allAgents.html'
			}
		})
	})

	$('.reject').click(function(){
		window.location.href = '/allAgents.html'		
	})
}