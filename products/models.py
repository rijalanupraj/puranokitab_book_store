from django.db import models
import random
from django.db.models import Q
import os
from django.db.models.signals import pre_save
from puranokitab.utils import unique_slug_generator
from django.urls import reverse
from django.contrib.auth.models import User

from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal
import math
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator



def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)

BOOK_CONDITION = (
    ('excellent','Excellent'),
    ('good','Good'),
    ('satisfactory','Satisfactory'),
    ('poor','Poor'),

)


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name,ext = os.path.splitext(base_name)
    return name,ext

# Create your models here.
def upload_image_path(instance,filename):
    new_filename = random.randint(1,3910209312)
    name,ext = get_filename_ext(filename)
    final_filename = f'{new_filename}{ext}'
    return f"products/{new_filename}/{final_filename}"

class ProductQuerySet(models.query.QuerySet):
    def featured(self):
        return self.filter(featured=True,active=True)

    def active(self):
        return self.filter(active=True)
    def search(self,query):
        lookups = Q(title__icontains=query)| Q(description__icontains=query) | Q(price__icontains=query ) |Q(tag__title__icontains=query)
        return self.filter(lookups).distinct()

class ProductManager(models.Manager):

    def get_queryset(self):
        return ProductQuerySet(self.model,using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self):
        return self.get_queryset().featured()

    def get_by_id(self,id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self,query):
        return self.get_queryset().active().search(query)



class Product(models.Model):
    seller = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    author = models.CharField(max_length=120)
    slug = models.SlugField(blank=True,null=True,unique=True)
    description = models.TextField()
    published_date = models.PositiveIntegerField(default=current_year(), validators=[MinValueValidator(1950), max_value_current_year])
    market_price = models.DecimalField(decimal_places=2,max_digits=7,default=0.0,validators=[MinValueValidator(Decimal('0.01'))])
    your_price = models.DecimalField(decimal_places=2,max_digits=7,default=0.0,validators=[MinValueValidator(Decimal('0.01'))])
    price = models.DecimalField(decimal_places=2,max_digits=7,default=0.0)
    book_condition = models.CharField(max_length=120,default='good',choices=BOOK_CONDITION)
    image = models.ImageField(upload_to=upload_image_path,null=True,blank=True,default='products/default_book.png')
    featured = models.BooleanField(default = False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ProductManager()    

    def get_absolute_url(self):
        return reverse("products:product-detail",kwargs={'slug':self.slug})

    def __str__(self):
        return self.title
    
    @property
    def name(self):
        return self.title


def product_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    calc = instance.your_price * Decimal(110/100)
    instance.price =  calc
pre_save.connect(product_pre_save_receiver,sender=Product)