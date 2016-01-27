window.onload=function(){
	main()
}
function main(){
	'use strict';

  	$(document).ready(function(){
		$('.tooltipped').tooltip({delay: 50});
	});

	$('#category-nav p').click(function(){

		$(".category-title").css('display','none');	
		$(".category-row").css('display','none');
		$("#category-nav p").removeClass("active-category");	
		$("#category-nav p").addClass("inactive-category");
		$(this).removeClass("inactive-category");	
		$(this).addClass("active-category");	
		var id=($(this).attr("id"));
		var categoryId =(id)+"-title";
		var categoryRow =(id)+"-content";
		$("#"+categoryId).css("display","block");
		$("#"+categoryRow).css("display","block");
	})

	$('.imageClass').click(function(){

		var url = "/";
		window.location.href=url;
	})
}

