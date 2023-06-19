$(document).ready(function(){
	$("#show_hide_password a").on('click', function(event) {
		event.preventDefault();
		if($('#show_hide_password input').attr("type") == "text"){
			$('#show_hide_password input').attr('type', 'password');
			$('#show_hide_password i').addClass( "fa-eye-slash" );
			$('#show_hide_password i').removeClass( "fa-eye" );
		}else if($('#show_hide_password input').attr("type") == "password"){
			$('#show_hide_password input').attr('type', 'text');
			$('#show_hide_password i').removeClass( "fa-eye-slash" );
			$('#show_hide_password i').addClass( "fa-eye" );
		}
	});

	$('#updateUserBtn').click(function(){
		updateUser()
		


	});

	function updateUser(){
		var inputUsername = $('#inputUsername').val()
		var inputFirstName = $('#inputFirstName').val()
		var inputLastName = $('#inputLastName').val()
		var inputEmailAddress = $('#inputEmailAddress').val()
		var role = $('#role').val()
		var passwordID = $('#passwordID').val()
		var profileImg = $('#profileImg')[0].files[0];
		var userId = $('#user_data').attr('user-id');
		console.log('User ID:', userId);

		var formData = new FormData();

		formData.append('inputUsername', inputUsername);
		formData.append('inputFirstName', inputFirstName);
		formData.append('inputLastName', inputLastName);
		formData.append('inputEmailAddress', inputEmailAddress);
		formData.append('passwordID', passwordID);
		formData.append('profileImg', profileImg);
		formData.append('userId', userId);

		fetchdata('/updateUserData',formData)
	}

})


function fetchdata(url, data) {
	$.ajax({
		url: url,
		data: data,
		method: 'POST',
		processData: false,
		contentType: false,
		beforeSend: function() {
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
	}).done(function(response) {
		$('#waitMeDiv').waitMe('hide');
		if (response === false) {
			SwalNotification('warning', 'Warning', 'Profile Not Found!');
		} else {
			SwalNotification('success', 'Success', 'Updated Successfully!', response);
		}
		return response;
	}).fail(function(response) {
		SwalNotification('error', 'Error', 'Failed to Update!', response);
		return response;
	});
}

function SwalNotification(icon, title, text, data) {
	Swal.fire({
		icon: icon,
		title: title,
		text: text + ' ' + data,
		showCancelButton: true,
		confirmButtonColor: '#3085d6',
		cancelButtonColor: '#d33',
		confirmButtonText: 'OK!'
	}).then((result) => {
		if (result.isConfirmed && icon === 'success') {
			Swal.fire('Updated!', 'Your Profile has been updated.', 'success');
			location.reload();
		}else{
			Swal.fire('Error!', 'Your Profile has not been updated.', 'warning');
			return false;
		}
	});
}

function CheckRole(role){

}