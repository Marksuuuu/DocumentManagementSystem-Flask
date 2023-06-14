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

		$.ajax({
			url: '/register',
			method: 'POST',
			data: formData,
			contentType: false,
			processData: false,
			beforeSend: function(){
				$('#waitMeDiv').waitMe({
					effect: 'rotateplane',
					text: 'Please wait...',
					bg: 'rgba(255,255,255,0.7)',
					color: '#435ebe',
					maxSize: '',
					waitTime: -1,
					textPos: 'vertical',
					fontSize: '',
					source: ''
				});

			},
			success: function(data){
				Swal.fire({
					icon: 'success',
					title: 'Registered!',
					showConfirmButton: true,
					text: 'Registered Successfully!.',
				})
				var personUsername = $('#personUsername').val('')
				var firstname = $('#personfirstName').val('')
				var lastname = $('#personlastName').val('')
				var email = $('#personEmail').val('')
				var password = $('#personPassword').val('')
				var repeat_password = $('#personRepeatPassword').val('')
				var role = $('#role').val('')
			},

		}).done(function (){
			$('#waitMeDiv').waitMe('hide');


		});
	}
});
