from django.shortcuts import render
from products.models import Product
from django.views.generic import ListView
# Create your views here.

class SearchProductView(ListView):
    # queryset = Product.objects.all()
    template_name = "search/view.html"

    def get_context_data(self,*args,**kwargs):
        context = super(SearchProductView,self).get_context_data(*args,**kwargs)
        context['query'] = self.request.GET.get('q')
        return context


    def get_queryset(self):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q',None)
        if query is not None:
            return Product.objects.search(query)
        return Product.objects.none()