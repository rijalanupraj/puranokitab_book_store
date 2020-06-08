from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

from orders.models import Order

class SalesView(LoginRequiredMixin,TemplateView):
    template_name = 'analytics/sales.html'

    def dispatch(self,*args,**kwargs):
        user = self.request.user
        if not user.is_staff:
            return HttpResponse("Not Allowed",status=401)
        return super(SalesView,self).dispatch(*args,**kwargs)
    
    def get_context_data(self,*args,**kwargs):
        context = super(SalesView,self).get_context_data(*args,**kwargs)
        qs = Order.objects.all()
        context['orders'] = qs
        return context


