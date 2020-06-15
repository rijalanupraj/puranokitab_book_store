from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import ListView,DetailView,CreateView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from products.models import Product
from .forms import UserUpdateForm,ProfileUpdateForm

# Create your views here.
class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = "user/user_detail.html"

    def get_context_data(self,*args,**kwargs):
        context = super(UserDetailView,self).get_context_data(*args,**kwargs)
        request = self.request
        username = self.kwargs['username']        
        user_products = Product.objects.all().filter(seller__username=username)
        context['user_products'] = user_products
        return context
        

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

def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('login')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form':u_form,
        'p_form':p_form,
    }
    return render(request,'user/profile.html',context)