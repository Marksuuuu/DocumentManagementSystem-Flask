$(document).ready(function(){
	$('#submitProductDetails').click(function (){
		uploadProduct()
	});

	$('#uploadBtn').click(function() {
		var file = $('#csvFile')[0].files[0];
		var formData = new FormData();
		formData.append('file', file);
		uploadUsingCsv('/process-csv', formData)
		
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

		uploadUsingInput('/upload', formData)

	}


})
function uploadUsingInput(url,data){
	$.ajax({
		url: url,
		data: data,
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


function uploadUsingCsv(url,data){
	$.ajax({
		url: url,
		data: data,
		type: 'POST',
		contentType: false,
		processData: false,
		success: function(data) {
			var lines = data.split('\n');

			$.each(lines, function(index, line) {
				var columns = line.split(',');

				$.each(columns, function(index, column) {
					console.log(column);
				});
			});
		},
		error: function() {
			console.log('Error occurred during CSV file upload.');
		}
	});

}

