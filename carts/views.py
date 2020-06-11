from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse

from addresses.forms import AddressForm
from addresses.models import Address

from billing.models import BillingProfile
from orders.models import Order
from products.models import Product
from .models import Cart


def cart_detail_api_view(request):
    cart_obj,new_obj = Cart.objects.new_or_get(request)
    products = [{"id":x.id,"url":x.get_absolute_url(),"name":x.name,"price":x.price,"image":x.image.url} for x in cart_obj.products.all()]
    cart_data = {"products":products,"subtotal":cart_obj.subtotal,"total":cart_obj.total}
    return JsonResponse(cart_data)
   


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, "carts/home.html", {"cart": cart_obj})


def cart_update(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Show message to user, product is gone?")
            return redirect("carts:cart-home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            product_added = False
        else:
            cart_obj.products.add(product_obj) # cart_obj.products.add(product_id)
            product_added = True
        request.session['cart_items'] = cart_obj.products.count()
       
        # return redirect(product_obj.get_absolute_url())
        if request.is_ajax():
            json_data = {
                "added":product_added,
                "removed": not product_added,
                'cartItemCount':cart_obj.products.count()
            }
            return JsonResponse(json_data)
    return redirect("carts:cart-home")


@login_required
def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("carts:cart-home")  
    

    address_form = AddressForm()
    shipping_address_id = request.session.get("shipping_address_id", None)

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"] 
            order_obj.save()
            
    if request.method == "POST":
        is_done = order_obj.check_done()
        if is_done:
            order_obj.mark_checkout()
            request.session['cart_items'] = 0
            del request.session['cart_id']
            return redirect("carts:checkout-success")
            
    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "address_form": address_form,
        "address_qs":address_qs,
    }
    return render(request, "carts/checkout.html", context)

def success_page(request):
    return render(request,'carts/success.html')