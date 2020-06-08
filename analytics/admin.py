from django.contrib import admin

from .models import ObjectViewed,UserSession
# Register your models here.
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ['__str__','user','ip_address']
    search_fields = ['user__username']

    class Meta:
        model = UserSession

class ObjectViewedAdmin(admin.ModelAdmin):
    list_display = ['__str__','user','ip_address','content_object']
    search_fields = ['user__username']

    class Meta:
        model = ObjectViewed

admin.site.register(ObjectViewed,ObjectViewedAdmin)
admin.site.register(UserSession,UserSessionAdmin)