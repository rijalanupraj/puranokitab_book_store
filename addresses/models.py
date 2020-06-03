from django.db import models

from billing.models import BillingProfile
# Create your models here.
class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile,on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=120,blank=True)
    address_line_2 = models.CharField(max_length=120,null=True,blank=True)
    city = models.CharField(max_length=120,default='Pokhara')
    district = models.CharField(max_length=120,default='Kaski')
    
    def __str__(self):
        return str(self.billing_profile)
