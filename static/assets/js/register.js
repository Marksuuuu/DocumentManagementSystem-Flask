$(document).ready(function(){
	$('#register').click(function(){
		register()
	});

	function register() {
		var personUsername = $('#personUsername').val()
		var firstname = $('#personfirstName').val()
		var lastname = $('#personlastName').val()
		var email = $('#personEmail').val()
		var password = $('#personPassword').val()
		var repeat_password = $('#personRepeatPassword').val()
		var role = $('#role').val()
		var fileInput = $('#personProfileImage')[0].files[0];

		var formData = new FormData()
		formData.append('fileInput', fileInput);
		formData.append('personUsername', personUsername);
		formData.append('firstname', firstname);
		formData.append('lastname', lastname);
		formData.append('email', email);
		formData.append('password', password);
		formData.append('role',role);

		
		console.log(role)

		$.ajax({
			url: '/register',
			method: 'POST',
			data: formData,
			contentType: false,
			processData: false,

			success: function(data){

			},

		});
	}
});
