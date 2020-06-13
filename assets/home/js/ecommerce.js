$(document).ready(function(){
    //Auto Search
    var searchForm = $('.search-form')
    var searchInput = searchForm.find("[name='q']")
    var typingTimer;
    var typingInterval = 500;
    var searchBtn = searchForm.find("[type='submit']")

    searchInput.keyup(function(event){
        //key released
        clearTimeout(typingTimer)
        typingTimer = setTimeout(performSearch,typingInterval);
    })
    searchInput.keydown(function(event){
        //keypressed
        clearTimeout(typingTimer)
    })
    
    function displaySearching(){
        searchBtn.addClass("disabled")
        searchBtn.html("<i class='fa fa-spin fa-spinner'></i>Searching...")
    }

    function performSearch(){
        displaySearching()
        var query = searchInput.val();
        setTimeout(function(){
        window.location.href = '/search/?q='+query;
        },1000)
    }

    //For cart update in products details page
  var productForm = $(".form-product-ajax-update") // #form-product-ajax

  productForm.submit(function(event){
      event.preventDefault();
      
      var thisForm = $(this)
     
      var actionEndpoint = thisForm.attr("data-endpoint")
      var httpMethod = thisForm.attr("method");
      var formData = thisForm.serialize();

      $.ajax({
        url: actionEndpoint,
        method: httpMethod,
        data: formData,
        success: function(data){
          var submitSpan = thisForm.find(".submit-span")
          if (data.added){
            submitSpan.html("<button type='submit' class='btn btn-warning btn-lg'>Remove</button><a href=\"{% url 'carts:cart-home' %}\"><button type=\"button\" class=\"btn btn-primary\">Go to cart <span class=\"badge badge-light\">{{request.session.cart_items}}</span></button></a>")
          } else {
            submitSpan.html("<button type='submit' class='btn btn-primary btn-lg'>Add to cart</button>")
           }
          var navbarCount = $(".navbar-cart-count")
          navbarCount.text(data.cartItemCount)
        },
        error: function(errorData){
            $.alert({
                title: "Oops!",
                content: "An error occured",
                theme:'modern'
            });
        }
      })
  })
})
$(document).ready(function(){
    //For cart delete
  var productForm = $(".form-product-ajax-update-nav") // #form-product-ajax

  productForm.submit(function(event){
      event.preventDefault();
      
      var thisForm = $(this)
      var actionEndpoint = thisForm.attr("data-endpoint")
      var httpMethod = thisForm.attr("method");
      var formData = thisForm.serialize();

      $.ajax({
        url: actionEndpoint,
        method: httpMethod,
        data: formData,
        success: function(data){
          var submitSpan = thisForm.find(".submit-span")
          var navbarCount = $(".navbar-cart-count")
          navbarCount.text(data.cartItemCount)
          var currentPath = window.location.href

          if (currentPath.indexOf("cart") != -1) {
            refreshCart()
          }
        },
        error: function(errorData){
            $.alert({
                title: "Oops!",
                content: "An error occured",
                theme:'modern'
            });
        }
      })

  })

  function refreshCart(){
    var cartTable = $(".cart-table")
    var cartBody = cartTable.find(".cart-body")
    var checkoutBody = $('.shoping__checkout')
    //cartBody.html("<h1>Changed</h1>")
    var productRows = cartBody.find(".cart-product")
    var currentUrl = window.location.href

    var refreshCartUrl = '/api/cart/'
    var refreshCartMethod = "GET";
    var data = {};
    $.ajax({
      url: refreshCartUrl,
      method: refreshCartMethod,
      data: data,
      success: function(data){
        if (data.products.length > 0){
            var hiddenCartItemRemoveForm = $('.cart-item-remove-form')
            productRows.html(" ")
            i = 1
            $.each(data.products, function(index, value){
              
              var newCartItemRemove = hiddenCartItemRemoveForm.clone()
              newCartItemRemove.css("display","block")
              newCartItemRemove.find(".cart-item-product-id").val(value.id)
                cartBody.prepend("<tr class=\"cart-product\"><td class=\"shoping__cart__item\"><img width=\"100\" height=\"100\" src="+"'"+ value.image+"'" +"alt=\"\"><a href=" + "'"+value.url+"'"+"><h5>"+ value.name +"</h5></a></td><td class=\"shoping__cart__price\">"+"Rs."+value.price +"</td><td class=\"shoping__cart__quantity\"><div class=\"quantity\"><div class=\"pro-qty\"> <input type=\"text\" value=\"1\"></div></div></td><td class=\"shoping__cart__total\">"+"Rs."+value.price+"</td><td class=\"shoping__cart__item__close\">"+newCartItemRemove.html()+"<td></tr>")
                i ++
            })
            
            checkoutBody.find(".cart-subtotal").text(data.subtotal)
            checkoutBody.find(".cart-total").text(data.total)
        } else {
          window.location.href = currentUrl
        }
        
      },
      error: function(errorData){
        $.alert({
            title: "Oops!",
            content: "An error occured",
            theme:'modern'
        });

      }
    })


  }



})