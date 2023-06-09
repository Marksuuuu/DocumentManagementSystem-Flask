$(document).ready(function() {
  gerResponse()

  $('#showCart').click(function(){
    $('#staticBackdrop').modal('show')
    var userId = $('p').attr('user-id');
    var url = '/showCart';
    var data = { userId : userId };

    showCartDetails(url, data)

  })


  function gerResponse(){
    $.get('/inventory', function(response) {
      if (response.data) {
        var inventoryData = response.data;

        $.each(inventoryData, function(index, item) {
          var card = $('<div style="width:300px">').addClass('card ');

          if (item.fileUploaded) {
            var image = $('<img>').addClass('card-img-top even-size').attr('src', item.fileUploaded);
          card.append(image); // Append the image to the card
        } else {
          var noImage = $('<img>').addClass('card-img-top even-size').attr('src', '/static/assets/img/products/No-Image-Placeholder.svg');
          card.append(noImage); // Append the "No Image" text to the card
        }

        var cardBody = $('<div>').addClass('card-body');

        $('<h5>').addClass('card-title').text(item.productName).appendTo(cardBody);

        $('<p>').addClass('card-text').text('Count: ' + item.productCount).appendTo(cardBody);

        $('<p>').addClass('card-text').text('Price: ' + item.productPrice).appendTo(cardBody);
        console.log(item.productPrice)

        $('<p>').addClass('card-text').text('Description: ' + item.productDescription).appendTo(cardBody);

        var itemId = $('<p>').addClass('test').css('display', 'none').text(item.id).appendTo(cardBody);

        var button = $('<button>').addClass('btn btn-primary').text('SHOW DETAILS');
        button.on('click', function() {
          // Call a function and pass the item data
          getData(item);
        });

        cardBody.append(button); // Append the button to the card body

        card.append(cardBody);

        card.appendTo('#itemContainer');
      });
      }
    });

  }

  $('#incrementCount').click(function() {
    var count = parseInt($('#productCount').val());
    $('#productCount').val(count + 1);
  });

  $('#decrementCount').click(function() {
    var count = parseInt($('#productCount').val());
    if (count > 1) {
      $('#productCount').val(count - 1);
    }
  });


  $('#addTOCart').click(function() {
    var itemImg = $('#itemImage').prop('src');
    var prodCount = $('#productCount').val();
    var productName = $('#productName').text();
    var productPrice = $('#productPrice').text();
    var data_id = $('#item-id').attr('item-id');
    var userId = $('p').attr('user-id');

  // Extract the image filename only
    var filename = itemImg.split('/').pop();


    console.log(prodCount, productName, productPrice, data_id, filename, userId);

    var formData = new FormData();

    formData.append('userId', userId);
    formData.append('data_id', data_id);
    formData.append('itemImg', filename);
    formData.append('prodCount', prodCount);
    formData.append('productName', productName);
    formData.append('productPrice', productPrice);

    addToCartInsert('/addtocart', formData);
  });



});

// Function to initialize DataTable
function initializeDataTable() {
  $('#cartTable').DataTable({
    lengthMenu: [[5, 10, 25, 50, -1], [5, 10, 25, 50, "All"]],
  });
}

// Function to populate table rows and initialize DataTable
function populateCartTable(responseData) {
  console.log('test', responseData);

  if (Array.isArray(responseData.data)) {
    // Clear the existing table rows
    $("#cartTable tbody").empty();

    responseData.data.forEach(function(item) {
      // Create a new row element
      var newRow = $("<tr>");

      // Add data to the row
      newRow.append("<td>" + item.ID + "</td>");
      newRow.append("<td>" + item.PRODPRICE + "</td>");
      newRow.append("<td>" + item.PRODNAME + "</td>");
      newRow.append("<td>" + item.PRODCOUNT + "</td>");
      newRow.append("<td><img src='" + item.FILEUP + "' alt='Profile Picture' width='70' height='70'></td>");
      newRow.append("<td>" + item.PRODDESC + "</td>");

      // Append the row to the table body
      $("#cartTable tbody").append(newRow);
    });

    // Check if DataTable is already initialized
    if (!$.fn.DataTable.isDataTable('#cartTable')) {
      // Initialize DataTable
      initializeDataTable();
    } else {
      // Destroy and reinitialize DataTable
      $('#cartTable').DataTable().destroy();
      initializeDataTable();
    }
  } else {
    console.error("Data is not an array:", responseData);
  }
}

// Main function to fetch data and populate table
function showCartDetails(url, data) {
  console.log('cluck');

  $.ajax({
    type: 'POST',
    url: url,
    data: JSON.stringify(data),
    contentType: 'application/json',
    processData: false,
    success: function(responseData) {
      populateCartTable(responseData);
    },
    error: function(jqXHR, textStatus, errorThrown) {
      console.error("AJAX request failed:", textStatus, errorThrown);
    }
  });
}




function addToCartInsert(url,data) {
  $.ajax({
    url: url,
    data: data,
    method: 'POST',
    processData: false,
    contentType: false,
    beforeSend: function() {
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



function getData(item) {
  var itemImg = $('#itemImage').attr('src', item.fileUploaded || '/static/assets/img/products/No-Image-Placeholder.svg');
  var prodName = $('#productName').text(item.productName);
  var prodCount =$('#productCount').text('Count: ' + item.productCount);
  var prodPrice =$('#productPrice').text('Price: ' + item.productPrice).attr('prod-price-data', item.productPrice);
  var prodDesc =$('#productDescription').text('Description: ' + item.productDescription);
  var data_id = $('#item-id').attr('item-id', item.id)
  $('#dataModal').modal('show');

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
      location.reload();
    }else{
      Swal.fire('Error!', 'Your Profile has not been updated.', 'warning');
      return false;
    }
  });
}

