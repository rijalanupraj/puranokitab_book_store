from django.shortcuts import render, Http404,get_object_or_404
from django.http import HttpResponseRedirect

from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import Product
from carts.models import Cart
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from products.models import Product


from analytics.mixins import ObjectViewedMixin
from django.contrib.contenttypes.models import ContentType

from comments.forms import CommentForm
from comments.models import Comment
# Create your views here.

class ProductListView(ListView):
    # queryset = Product.objects.all()
    template_name = "products/shop.html"
    paginate_by = 30

    def get_queryset(self):
        request = self.request
        return Product.objects.all()

    def get_context_data(self,*args,**kwargs):
        context = super(ProductListView,self).get_context_data(*args,**kwargs)
        request = self.request
        featured_prodcut = Product.objects.featured()
        context['featured_product'] = featured_prodcut
        return context

class ProductFeaturedListView(ListView):
    queryset = Product.objects.all().featured()
    template_name = "products/products_list_featured.html"


class ProductDetailView(ObjectViewedMixin, DetailView):
    queryset = Product.objects.all()
    template_name = "products/products_detail.html"
    slug_url_kwarg = 'slug'

    def post(self,*args, **kwargs):
        comment_form = CommentForm(self.request.POST)
        if comment_form.is_valid():
            print(comment_form.cleaned_data)
            c_type = comment_form.cleaned_data.get("content_type")
            content_type = ContentType.objects.get_for_model(Product)
            obj_id = comment_form.cleaned_data.get("object_id")
            content_data = comment_form.cleaned_data.get("content")
            parent_obj = None
            try:
                parent_id = int(self.request.POST.get("parent_id"))
            except:
                parent_id = None

            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count()==1:
                    parent_obj = parent_qs.first()

            new_comment,created = Comment.objects.get_or_create(
                user = self.request.user,
                content_type = content_type,
                object_id = obj_id,
                content = content_data,
                parent = parent_obj,
            )
            return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

        else:
            self.object = self.get_object()
            context = super().get_context_data(**kwargs)
            context['comment_form'] = comment_form


            return self.render_to_response(context=context)

    def get_context_data(self,*args,**kwargs):
        context = super(ProductDetailView,self).get_context_data(*args,**kwargs)
        request = self.request
        slug = self.kwargs['slug']
        cart_obj,new_obj = Cart.objects.new_or_get(request)
        
        instance =  get_object_or_404(Product,slug=slug)
        initial_data = {"content_type": instance.get_content_type,"object_id": instance.id}
        comment_form = CommentForm(request.POST or None, initial=initial_data)
        comments = instance.comments
        users_other_products = Product.objects.all().order_by('?')[:10]
        context['cart'] = cart_obj
        context['comments'] = comments
        context['comment_form'] = comment_form
        context['users_other_products'] = users_other_products
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
    fields = ['title','author','publication','market_price','your_price','book_condition','description','address','image',]
    template_name = 'products/product_form.html'

    def form_valid(self,form):
        form.instance.seller = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Product
    fields = ['title','author','publication','market_price','your_price','book_condition','description','address','image']
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