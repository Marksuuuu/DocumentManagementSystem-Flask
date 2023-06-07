$(document).ready(function(){
	$('#login').click(function(){
		login()
	});

	function login() {
		var username = $('#personUsername').val()
		var password = $('#personPassword').val()
		

		var formData = new FormData();
		formData.append('username',username);
		formData.append('password', password);

		$.ajax({
			url:'/login',
			data:formData,
			method: 'POST',
			contentType: false,
			processData: false,
			success: function(){

			}
		});

	}
});