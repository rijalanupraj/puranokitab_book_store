from django.urls import path
from . import views

urlpatterns = [
    path('',views.ProductListView.as_view(),name='products-main-page'),
    path('<str:slug>/',views.ProductDetailView.as_view(),name='product-detail'),
    path('featured/',views.ProductFeaturedListView.as_view(),name='fddf'),
]
app_name = 'products'