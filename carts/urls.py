from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('',views.cart_home,name='carts-home'),
]

app_name='carts'