$(document).ready(function(){
	$('#submitProductDetails').click(function (){
		uploadProduct()
	});

	function uploadProduct(){
		var productName = $('#productName').val();
		var productCount = $('#productCount').val();
		var fileUploaded = $('#fileUploaded')[0].files[0];
		var productPrice = $('#productPrice').val();
		var productTypes = $('#productTypes').val();
		var productDescription = $('#productDescription').val();

		var formData = new FormData();
		formData.append('productName', productName);
		formData.append('productCount', productCount);
		formData.append('fileUploaded', fileUploaded);
		formData.append('productPrice', productPrice);
		formData.append('productDescription', productDescription);
		formData.append('productTypes', productTypes);

		$.ajax({
			url: '/upload',
			data: formData,
			method: 'POST',
			contentType: false,
			processData: false,
			beforeSend: function(){

			},
			success: function(){

			},
		}).done(function(){

		})
	}
})