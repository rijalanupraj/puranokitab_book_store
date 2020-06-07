from django.shortcuts import render, Http404
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import Product
from carts.models import Cart
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from products.models import Product

from analytics.mixins import ObjectViewedMixin

# Create your views here.

class ProductListView(ListView):
    # queryset = Product.objects.all()
    template_name = "products/shop.html"
    paginate_by = 30

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

class ProductCreateView(LoginRequiredMixin,CreateView):
    model = Product
    fields = ['title','author','market_price','your_price','book_condition','description','image']
    template_name = 'products/product_form.html'

    def form_valid(self,form):
        form.instance.seller = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Product
    fields = ['title','author','market_price','your_price','book_condition','description','image']
    template_name = 'products/product_form.html'

    def form_valid(self,form):
        form.instance.seller = self.request.user
        return super().form_valid(form)

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.seller:
            return True
        return False

class ProductDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.seller:
            return True
        return False