from django.conf import settings
from django.db import models
from products.models import Product
from django.db.models.signals import pre_save, post_save,m2m_changed
User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
   
    #Seen tutorial cart not assoicated to authenticated user
    # def new_or_get(self, request):
    #     cart_id = request.session.get("cart_id", None)
    #     qs = self.get_queryset().filter(id=cart_id)
    #     if qs.count() == 1:
    #         new_obj = False
    #         cart_obj = qs.first()
    #         if request.user.is_authenticated and cart_obj.user is None:
    #             cart_obj.user = request.user
    #             cart_obj.save()
    #     else:
    #         cart_obj = Cart.objects.new(user=request.user)
    #         new_obj = True
    #         request.session['cart_id'] = cart_obj.id
    #     return cart_obj, new_obj
    
    #cart authenticated to all user but not loggined user can't retrieve cart after login
    # def new_or_get(self, request):
    #     if request.user.is_authenticated:
    #         qs = self.get_queryset().filter(user__username=request.user.username,active=True)
    #         if qs.count() == 1:
    #             new_obj = False
    #             cart_obj = qs.first()
    #             print(cart_obj.products.all().count())
    #             request.session['cart_id'] = cart_obj.id
    #         else:
    #             cart_obj = Cart.objects.new(user=request.user)
    #             new_obj = True
    #             request.session['cart_id'] = cart_obj.id
    #     else:
    #         cart_id = request.session.get("cart_id", None)
    #         qs = self.get_queryset().filter(id=cart_id)
    #         if qs.count() == 1:
    #             new_obj = False
    #             cart_obj = qs.first()
    #             if request.user.is_authenticated and cart_obj.user is None:
    #                 cart_obj.user = request.user
    #                 cart_obj.save()
    #         else:
    #             cart_obj = Cart.objects.new(user=request.user)
    #             new_obj = True
    #             request.session['cart_id'] = cart_obj.id
    #     return cart_obj, new_obj

    def new_or_get(self, request):
        if request.user.is_authenticated:
            qs = self.get_queryset().filter(user__username=request.user.username,active=True)
            if qs.count() == 1:
                new_obj = False
                cart_obj = qs.first()
                request.session['cart_id'] = cart_obj.id
            else:
                cart_id = request.session.get("cart_id", None)
                qs = self.get_queryset().filter(id=cart_id)
                if qs.count() == 1:
                    new_obj = False
                    cart_obj = qs.first()
                    if cart_obj.user is None:
                        cart_obj.user = request.user
                        cart_obj.save()

                else:
                    cart_obj = Cart.objects.new(user=request.user)
                    new_obj = True
            request.session['cart_id'] = cart_obj.id
            

        else:
            cart_id = request.session.get("cart_id", None)
            qs = self.get_queryset().filter(id=cart_id)
            if qs.count() == 1:
                new_obj = False
                cart_obj = qs.first()
                if request.user.is_authenticated and cart_obj.user is None:
                    cart_obj.user = request.user
                    cart_obj.save()
            else:
                cart_obj = Cart.objects.new(user=request.user)
                new_obj = True
                request.session['cart_id'] = cart_obj.id
        request.session['cart_items'] = cart_obj.products.count()
        return cart_obj, new_obj


    def new(self,user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj=user
        return self.model.objects.create(user=user_obj)

class Cart(models.Model):
    user = models.ForeignKey(User, null=True,blank=True,on_delete=models.CASCADE)
    products = models.ManyToManyField(Product,blank=True)
    total = models.DecimalField(default=0.0,max_digits=60,decimal_places=2)
    subtotal = models.DecimalField(default=0.0,max_digits=60,decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


    objects = CartManager()

    def __str__(self):
        return str(self.id)

                    

def m2m_changed_cart_receiver(sender,instance,action,*args,**kwargs):
    if action=='post_add' or action =='post_remove' or action =='post_clear':
        products = instance.products.all()
        total = 0
        for x in products:
            total += x.price
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()
    

m2m_changed.connect(m2m_changed_cart_receiver,sender=Cart.products.through)

def pre_save_cart_receiver(sender,instance,*args,**kwargs):
    instance.total = instance.subtotal

pre_save.connect(pre_save_cart_receiver,sender=Cart)