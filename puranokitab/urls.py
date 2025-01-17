"""affnokitab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from addresses.views import checkout_address_create_view,checkout_address_reuse_view
from carts.views import cart_detail_api_view
from user import views
# from comments.views import comment

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('accounts.urls')),
    path('',include('home.urls')),
    path('products/', include('products.urls',namespace='products')),
    path('search/',include('search.urls',namespace='search')),
    path('cart/',include('carts.urls',namespace='carts')),
    path('checkout/address/create/',checkout_address_create_view,name='checkout_address_create'),
    path('checkout/address/reuse/',checkout_address_reuse_view,name='checkout_address_reuse'),
    path('api/cart/',cart_detail_api_view,name="api-cart"),
    path('analytics/',include('analytics.urls',namespace='analytics')),
    path('user/',include('user.urls',namespace='user')),

    
]
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
