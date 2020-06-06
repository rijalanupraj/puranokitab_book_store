from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import ListView,DetailView,CreateView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from products.models import Product

# Create your views here.
class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = "user/user_detail.html"

    def get_object(self):

        object = get_object_or_404(User, username=self.kwargs.get("username"))

        # only owner can view his page
        if self.request.user.username == object.username:
            return object
        else:
            # redirect to 404 page
            print("you are not the owner!!")

class ProductCreateView(LoginRequiredMixin,CreateView):
    model = Product
    fields = ['title','author','market_price','price','book_condition','description','image']
    template_name = 'user/product_form.html'

    def form_valid(self,form):
        form.instance.seller = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin,UpdateView):
    model = Product
    fields = ['title','author','market_price','price','book_condition','description','image']
    template_name = 'user/product_form.html'

    def form_valid(self,form):
        form.instance.seller = self.request.user
        return super().form_valid(form)