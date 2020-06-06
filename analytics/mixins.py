from .signals import object_viewed_signal

class ObjectViewedMixin(object):
    def get_context_data(self,*args,**kwargs):
        context = super(ObjectViewedMixin,self).get_context_data(*args,**kwargs)
        request = self.request
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None
        instance = context.get('object')
        if instance:
            object_viewed_signal.send(instance.__class__, instance=instance,request=request,user=user)
        return context
    
    
