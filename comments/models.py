from django.db import models
from django.contrib.auth.models import User
from products.models import Product
# Create your models here.

class Comment(models.Model):
    message = models.TextField('Leave a comment',max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
