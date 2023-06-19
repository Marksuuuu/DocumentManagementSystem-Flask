$(document).ready(function() {
  $.get('/inventory', function(response) {
    if (response.data) {
      var inventoryData = response.data;

      $.each(inventoryData, function(index, item) {
        var card = $('<div>').addClass('card');

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

        $('<p>').addClass('card-text').text('Price: $' + item.productPrice).appendTo(cardBody);

        $('<p>').addClass('card-text').text('Description: ' + item.productDescription).appendTo(cardBody);

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
});

function getData(item) {
  // Function to handle button click and retrieve data
  $('#itemImage').attr('src', item.fileUploaded || '/static/assets/img/products/No-Image-Placeholder.svg');
  $('#productName').text(item.productName);
  $('#productCount').text('Count: ' + item.productCount);
  $('#productPrice').text('Price: $' + item.productPrice);
  $('#productDescription').text('Description: ' + item.productDescription);

  $('#dataModal').modal('show');
}
