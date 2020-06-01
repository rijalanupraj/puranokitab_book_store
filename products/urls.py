from django.urls import path
from . import views

urlpatterns = [
    path('',views.ProductListView.as_view(),name=''),
    path('<str:slug>/',views.ProductDetailView.as_view(),name=''),
    path('featured/',views.ProductFeaturedListView.as_view(),name='fddf'),
]