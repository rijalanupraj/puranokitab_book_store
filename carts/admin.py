from django.contrib import admin

from .models import Cart
# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ['__str__','user','total']
    search_fields = ['user__username']

    class Meta:
        model = Cart


admin.site.register(Cart,CartAdmin)