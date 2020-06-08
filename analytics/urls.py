from django.urls import path,include
from . import views 

urlpatterns = [
    path('sales',views.SalesView.as_view(),name = 'sales'),
]

app_name = 'analytics'