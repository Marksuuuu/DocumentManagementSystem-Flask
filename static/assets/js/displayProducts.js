$(document).ready(function (){
	displayDataTbl()


	function displayDataTbl() {
		var table = $('#productContainer').DataTable({
			ajax: '/inventory',
			processing: true,
			lengthMenu: [[5, 10, 25, 50, -1], [5, 10, 25, 50, "All"]],
			columns: [
				{ data: 'id' },
				{ data: 'productName' },
				{ data: 'productCount' },

				{
					data: 'fileUploaded',
					render: function (data) {
						if(data == ''){
							return '<img src="/static/assets/img/products/No-Image-Placeholder.svg" alt="Profile Picture" width="70" height="70">'
						}else{
							return '<img src="' + data + '" alt="Profile Picture" width="70" height="70">';
						}
					}
				},

				{ data: 'productPrice' },
				{ data: 'productDescription' },
				{ data: 'productTypes' },
				{
					data: null,
					render: function (data, type, row) {
						return '<button type="button" class="btn btn-success rounded-pill fa-solid fa-pen edit-btn" data-id="' + row.id + '"></button> ' +
						'<button type="button" class="btn btn-danger rounded-pill fa-solid fa-trash delete-btn" data-id="' + row.id + '"></button> ';
						
					}
				},
				]
			
		})

		$('#productContainer').on('click', '.delete-btn', function(){
			Swal.fire({
				title: 'Are you sure?',
				text: "You won't be able to revert this!",
				icon: 'warning',
				showCancelButton: true,
				confirmButtonColor: '#3085d6',
				cancelButtonColor: '#d33',
				confirmButtonText: 'Yes, delete it!'
			}).then((result) => {
				if (result.isConfirmed) {
					var id = $(this).attr('data-id');
					var url = '/deleteProducts';
					var data = { id: id };
					ajaxRequest(url, data);
				}
			})
			
			
		})
		$('#productContainer').on('click', '.edit-btn', function(){
			var id = $(this).attr('data-id');
			var url = '/updateProducts';
			var data = { id: id };
			console.log(id)
			// ajaxRequest(url, data);
		})
	}
})

function ajaxRequest(url, data) {
	$.ajax({
		type: 'POST',
		url: url,
		data: JSON.stringify(data),
		contentType: 'application/json',
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
		success: function(response) {
			Swal.fire({
				icon: 'success',
				title: 'Deleted!',
				showConfirmButton: true,
				text: 'Delete Successfully!.',
			})
			$('#productContainer').DataTable().ajax.reload();
		},
		error: function(xhr, status, error) {
			console.log('AJAX request failed');
			console.log(xhr.responseText);
		}
	}).done(function (){
		$('#waitMeDiv').waitMe('hide');

	})
}
