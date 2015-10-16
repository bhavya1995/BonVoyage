window.onload=function(){
	main()
}
function main(){
	'use strict';

	$('#submitReq').click(function(){

		var ratingAgent= $('#input-id1').val();
		var ratingUs= $('#input-id2').val();
		var review= $('#review').val();
		var id=$("#submitReq").parent().attr("id");

		$.ajax({
			type: 'GET',
			url: '/submitFeedback',
			data: {
				ratingAgent:ratingAgent,
				ratingUs:ratingUs,
				review:review,
				id:id
			},
			success: function(data){
				
				var url="/dashboardTraveller";
				window.location=url;
			}
		});
	})
}