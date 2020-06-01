from django.shortcuts import render, Http404
from django.views.generic import ListView,DetailView
from .models import Product
# Create your views here.

class ProductListView(ListView):
    # queryset = Product.objects.all()
    template_name = "products/shop.html"

    def get_queryset(self):
        request = self.request
        return Product.objects.all()

class ProductFeaturedListView(ListView):
    queryset = Product.objects.all().featured()
    template_name = "products/products_list_featured.html"


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/products_detail.html"
    slug_url_kwarg = 'slug'
    
    # def get_queryset(self,*args,**kwargs):
    #     request = self.request
    #     pk = self.kwargs.get('pk')
    #     return Product.objects.filter(pk=pk)

