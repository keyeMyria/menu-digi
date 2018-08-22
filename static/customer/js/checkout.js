var fadeTime = 300;
var socketState = false;


function toast(text) {
    $("#snackbar").text(text)
    $("#snackbar").addClass("show")
    setTimeout(function(){ $("#snackbar").removeClass("show"); }, 3000);
}

window.onload= recalculateCart()
var Food = function(id,name,price,quantity){
    this.id=id
    this.name=name
    this.price=price
    this.quantity=quantity
}
var cartItems=[]

var removeFoodObjById = function(foodId){
    for (var i=0; i<cartItems.length; i++){
        if (cartItems[i].id===foodId){
            cartItems.splice(i,1)
            return true
        }
    }
    return false
}
var updateFoodObjQuantity = function(foodId,quantity){
    for (var i=0; i<cartItems.length; i++){
        if (cartItems[i].id===foodId){
            cartItems[i].quantity = parseInt(quantity)
            return true
        }
    }
    return false
}

var checkDuplicate = function(foodObj){
    for (var i=0; i<cartItems.length; i++){
        if (cartItems[i].id===foodObj.id){
            cartItems[i].quantity +=1
            return true
        }
    }
    cartItems.push(foodObj)
    return false
}

$(".add-cart-btn").click(function(){
    var id = parseInt($(this).parent().children(".food-id").text())
    var name=$(this).parent().children(".food-name").text()
    var price= parseFloat($(this).parent().children(".food-price").text())
    var foodItem= new Food(id,name,price,1)
    checkDuplicate(foodItem)
    updateDomCart()
    console.log($(this).parent().children(".food-price").text())
})

/* Assign actions */
$('.product-quantity input').change( function() {
  updateQuantity(this);
});

$('.product-removal button').click( function() {
    console.log("pressed")
  removeItem(this);
});



/* Recalculate cart */
function recalculateCart()
{
  var subtotal = 0;
  
  /* Sum up row totals */
  $('.product').each(function () {
    subtotal += parseFloat($(this).children('.product-line-price').text());
  });
  
  /* Calculate totals */
//   var tax = subtotal * taxRate;
//   var shipping = (subtotal > 0 ? shippingRate : 0);
  var total = subtotal;
  
  /* Update totals display */
  $('.totals-value').fadeOut(fadeTime, function() {
    $('#cart-total').html(total.toFixed(2));
    if(total == 0){
      $('.checkout-submit').fadeOut(fadeTime);
    }else{
      $('.checkout-submit').fadeIn(fadeTime);
    }
    $('.totals-value').fadeIn(fadeTime);
  });
}


/* Update quantity */
function updateQuantity(quantityInput)
{
  /* Calculate line price */
  var productRow = $(quantityInput).parent().parent();
  var price = parseFloat(productRow.children('.product-price').text());
  var productId =parseInt(productRow.children('.product-uid').text())
  var quantity = $(quantityInput).val();
  if( parseInt(quantity)===0){
      removeFoodObjById(productId)
      updateDomCart()
      return false
  }
  updateFoodObjQuantity(productId,quantity)
  var linePrice = price * quantity;
  
  /* Update line price display and recalc cart totals */
  productRow.children('.product-line-price').each(function () {
    $(this).fadeOut(fadeTime, function() {
      $(this).text(linePrice.toFixed(2));
      recalculateCart();
      $(this).fadeIn(fadeTime);
    });
  });  
}


/* Remove item from cart */
function removeItem(removeButton){
  /* Remove row from DOM and recalc cart total */
  var productId= parseInt($(removeButton).parent().parent().children(".product-uid").text())
  console.log(productId)
  var productRow = $(removeButton).parent().parent();
  removeFoodObjById(productId)
  productRow.slideUp(fadeTime, function() {
    productRow.remove();
    recalculateCart();
  });
  updateDomCart()

}

function updateDomCart(){
    $(".food-cart-items").empty()
    for(var i=0;i<cartItems.length;i++){
        $(".food-cart-items").append(`
        <tr class="product">
            <th scope="row" class="product-uid">`+cartItems[i].id+`</th>
            <td class="product-title">`+cartItems[i].name+`</td>
            <td class="product-price">`+parseFloat(cartItems[i].price)+`</td>
            <td class="product-quantity">
                    <input type="number" value="`+parseInt(cartItems[i].quantity)+`" min="1">
            </td>
            <td class="product-removal">                         
                <button class="remove-product">
                    Remove
                </button>
            </td>
            <td class="product-line-price">`+parseInt(cartItems[i].quantity)*parseFloat(cartItems[i].price)+`</td>
        </tr>`
      )
    }
    $('.product-removal button').click( function() {
        console.log("pressed")
      removeItem(this);
    });
    $('.product-quantity input').change( function() {
        updateQuantity(this);
    });
    recalculateCart();

}


  var loc = window.location
  var wsStart = "ws://"
  if (loc.protocol == "https:"){
      wsStart = "wss://"
  }
  var webSocketEndpoint =  wsStart + loc.host + appConfig.socketEndpoint  // ws : wss
  
  var socket = new ReconnectingWebSocket(webSocketEndpoint)
  
  
  socket.onmessage = function(e){
    console.log("message",e)
    data = JSON.parse(e.data)
    if(data["status"]==true){
        toast(data["message"])
    }
  }
  
  socket.onclose = function(e){
    socketState = false
    console.log("close",e)
  }
  
  socket.onopen = function(e){
    socketState = true
    toast("connection established")
    console.log("opened",e)
    $("#cartForm").submit(function(event){
        event.preventDefault();
        var username = $("#cart-username").val()
        var contact = $("#cart-contact").val()
        var email = $("#cart-email").val()
        var message = $("#cart-message").val()
        var table = appConfig.tableId
        var data = JSON.stringify({username:username,contact:contact,email:email,message:message,table:table,foods:cartItems,event:"Order"})
        socket.send(data)
        $(':input',"#cartForm")
        .not(':button, :submit, :reset, :hidden')
        .val('')
        .prop('checked', false)
        .prop('selected', false);
        // $(this)[0].reset()
      })
  }
  
  socket.onerror = function(e){
    console.log("error",e)
  }