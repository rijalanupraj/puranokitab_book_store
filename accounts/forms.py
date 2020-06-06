from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.core.exceptions import ValidationError


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=100)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']

    def clean(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(" Email exists")
        elif User.objects.filter(username=username).exists():
            raise forms.ValidationError(f"{username} Username Already Taken")
        return self.cleaned_data

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')

    