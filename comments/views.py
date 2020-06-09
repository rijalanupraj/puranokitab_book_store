from django.shortcuts import render,redirect
from .models import Comment

# Create your views here.
def comment(request,id):
    if request.POST:
        message = request.POST['message']
        user_id = request.POST['user_id']
        slug = request.POST['slug']
        product_id = id
        print(message)
        if len(message) <=5 :
            return redirect("products:product-detail",slug=slug)

        query = Comment(message=message)
        query.product_id = product_id
        query.user_id = user_id
        query.save()

    return redirect("products:product-detail",slug=slug)
    
    
    
