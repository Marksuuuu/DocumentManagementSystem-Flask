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
						return '<img src="' + data + '" alt="Profile Picture" width="50" height="50">';
					}
				},

				{ data: 'productPrice' },
				{ data: 'productDescription' },
				{ data: 'productTypes' },
				{
					data: null,
					render: function (data, type, row) {
						return '<button type="button" class="btn btn-success rounded-pill fa-solid fa-pen edit-btn" data-id="' + row.id + '"></button> ' +
						'<button type="button" class="btn btn-danger rounded-pill fa-solid fa-trash stop-btn" data-id="' + row.id + '"></button> ';
						
					}
				},
				]
			
		})

		$('#productContainer').on('click', '.edit-btn', function(){
			var id = $(this).attr('data-id');
			editProducts(id)
			
		})
		$('#productContainer').on('click', '.stop-btn', function(){
			var id = $(this).attr('data-id');
			deleteProducts(id)
		})
	}

	function editProducts(data){
		var id = data
		var formData = new FormData()
		formData.append('id', id)

		ajaxRequest('/editProducts', formData)
		console.log('toggled, edit', id)

	}
	function deleteProducts(data){
		var id = data
		var formData = new FormData()
		formData.append('id', id)

		ajaxRequest('/deleteProducts', data)
		console.log('toggled, ', id)
	}

	function ajaxRequest(url,data) {
		$.ajax({
			url: url,
			type: 'POST',
			data: data,
			processData: false,
			contentType: false,
			beforeSend: function(){

			},
			success: function(){

			}
		}).done(function (){

		})
		
	}
})