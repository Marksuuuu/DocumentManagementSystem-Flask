$(document).ready(function(){
	$('#login').click(function(){
		login()
	});

	function login() {
		var email = $('#personEmail').val()
		var password = $('#personPassword').val()
		console.log(password)

	}
});