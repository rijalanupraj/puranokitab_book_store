from django.urls import path
from . import views

urlpatterns = [
    path('',views.ProductListView.as_view(),name='products-main-page'),
    path('new/book',views.ProductCreateView.as_view(),name='new-product'),
    path('<str:slug>/',views.ProductDetailView.as_view(),name='product-detail'),
    path('featured/',views.ProductFeaturedListView.as_view(),name='fddf'),
    path('<str:slug>/update',views.ProductUpdateView.as_view(),name='product-update'),
    path('<str:slug>/delete',views.ProductDeleteView.as_view(),name='product-delete'),

    ]
app_name = 'products'