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


    var itemImg = $('#itemImage').prop('src')
    var prodCount = $('#productCount').val()
    var productName = $('#productName').text()
    var productPrice = $('#productPrice').text()
    var data_id = $('#item-id').attr('item-id')
    console.log(prodCount, productName, productPrice, data_id)

    var formData = new FormData()

    formData.append('itemImg', itemImg);
    formData.append('prodCount', prodCount);
    formData.append('productName', productName);
    formData.append('productPrice', productPrice);


    // addToCartInsert('/addtocart', formData)
  });



});


function getData(item) {
  var itemImg = $('#itemImage').attr('src', item.fileUploaded || '/static/assets/img/products/No-Image-Placeholder.svg');
  var prodName = $('#productName').text(item.productName);
  var prodCount =$('#productCount').text('Count: ' + item.productCount);
  var prodPrice =$('#productPrice').text('Price: $' + item.productPrice);
  var prodDesc =$('#productDescription').text('Description: ' + item.productDescription);
  var data_id = $('#item-id').attr('item-id', item.id)
  $('#dataModal').modal('show');

}

function addToCartInsert(url,data) {
  $.ajax({
    url: url,
    data: data,
    method: 'POST',
    processData: false,
    contentType: false,
    beforeSend: function(){

    },
    success: function(){

    }
  }).done(function(){

  })
}


