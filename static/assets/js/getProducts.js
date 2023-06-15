$(document).ready(function() {
  $.get('/inventory', function(response) {
    if (response.data) {
      var inventoryData = response.data;

      $.each(inventoryData, function(index, item) {
        var card = $('<div>').addClass('card');

        var cardBody = $('<div>').addClass('card-body');

        $('<h5>').addClass('card-title').text(item.productName).appendTo(cardBody);

        $('<p>').addClass('card-text').text('Count: ' + item.productCount).appendTo(cardBody);

        $('<p>').addClass('card-text').text('Price: $' + item.productPrice).appendTo(cardBody);

        $('<p>').addClass('card-text').text('Description: ' + item.productDescription).appendTo(cardBody);

        var button = $('<button>').addClass('btn btn-primary').text('Get Data');
        button.on('click', function() {
          // Call a function and pass the item data
          getData(item);
        });

        cardBody.append(button); // Append the button to the card body

        cardBody.appendTo(card);

        card.appendTo('#itemContainer');
      });
    }
  });
});

function getData(item) {
  // Function to handle button click and retrieve data
  console.log('Product Name:', item.productName);
  console.log('Product Count:', item.productCount);
  console.log('Product Price:', item.productPrice);
  console.log('Product Description:', item.productDescription);
}
