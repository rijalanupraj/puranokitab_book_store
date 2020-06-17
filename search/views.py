from django.shortcuts import render
from products.models import Product
from django.views.generic import ListView
# Create your views here.
from decimal import Decimal as D

class SearchProductView(ListView):
    # queryset = Product.objects.all()
    template_name = "search/view.html"

    def get_context_data(self,*args,**kwargs):
        context = super(SearchProductView,self).get_context_data(*args,**kwargs)
        context['query'] = self.request.GET.get('q')
        context['district'] = self.request.GET.get('district')
        return context


    def get_queryset(self):
        request = self.request
        method_dict = request.GET
        print(method_dict)
        query = method_dict.get('q',None)
        minamount = method_dict.get('minamount',None)
        maxamount = method_dict.get('maxamount',None)
        district = method_dict.get('district',None)
        if minamount is not None and maxamount is not None:
            minamount = minamount[4:]
            maxamount = maxamount[4:]
        print(district)

        if query is not None and query != '':
            return Product.objects.search(query,district,minamount,maxamount)
        elif minamount is not None and maxamount is not None and district is not None and district !='' and district !='None':
            return Product.objects.search_by_district_price(district,minamount,maxamount)
        elif minamount is not None and maxamount is not None:
            return Product.objects.search_by_price(minamount,maxamount)
        return Product.objects.none()