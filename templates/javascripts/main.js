$(document).ready(function(){
	$('#reader').html5_qrcode(function(data){
              $.post('/scancode', {"data":data});
		},
		function(error){
			$('#read_error').html(error);
		}, function(videoError){
			$('#vid_error').html(videoError);
		}
	);
});
