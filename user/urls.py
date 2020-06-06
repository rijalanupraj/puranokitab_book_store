from django.urls import path

from . import views

urlpatterns = [
    path('<str:username>/',views.UserDetailView.as_view(), name='user_detail'),
]

app_name = 'user'