from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserRegistrationForm
from .forms import LoginForm
from django.contrib import messages


from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .token_generator import account_activation_token
from django.contrib.auth.models import User

from django.contrib.auth import views as auth_views



# Create your views here.

def register(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'
            message = render_to_string('accounts/activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject,message, to=[to_email])
            email.send()
            messages.success(request,f'We have sent you an email, please confirm your email address to complete registration')
            return redirect('index')

    else:
        form = UserRegistrationForm()
    return render(request,'accounts/register.html',{'form':form})


def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request,f'Your account has been activated successfully')
        return redirect('index')
    else:
        return HttpResponse('Activation link is invalid!')

class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user=True