from django import forms

from .models import Comment

class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    parent_id = forms.IntegerField(widget=forms.HiddenInput,required=False)
    content = forms.CharField(label='',widget=forms.Textarea)
    # class Meta:
    #     model = Comment
    
    #     fields = [ 
    #     'content_type','object_id','content','parent_id',
    #     ]

