from django.shortcuts import render, Http404
from django.views.generic import ListView,DetailView
from .models import Product
from carts.models import Cart

from analytics.mixins import ObjectViewedMixin

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


class ProductDetailView(ObjectViewedMixin, DetailView):
    queryset = Product.objects.all()
    template_name = "products/products_detail.html"
    slug_url_kwarg = 'slug'

    def get_context_data(self,*args,**kwargs):
        context = super(ProductDetailView,self).get_context_data(*args,**kwargs)
        request = self.request
        cart_obj,new_obj = Cart.objects.new_or_get(request)
        context['cart'] = cart_obj
        return context
    
    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        #instance = get_object_or_404(Product, slug=slug, active=True)
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Not found..")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Uhhmmm ")
        return instance
    
    # def get_queryset(self,*args,**kwargs):
    #     request = self.request
    #     pk = self.kwargs.get('pk')
    #     return Product.objects.filter(pk=pk)

