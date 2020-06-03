from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('',views.cart_home,name='cart-home'),
    path('update/',views.cart_update,name='update'),
    path('checkout/',views.checkout_home,name='checkout'),

]

app_name='carts'