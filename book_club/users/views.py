from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token

User = get_user_model()

# send email with verification link
def verify_email(request):
    if request.method == "POST":
        if request.user.email_is_verified != True:
            current_site = get_current_site(request)
            user = request.user
            email = request.user.email
            subject = _("Verify Email")
            message = render_to_string('users/authentication/emails/verify_email_message.html', {
                'request': request,
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            email = EmailMessage(
                subject, message, to=[email]
            )
            email.content_subtype = 'html'
            email.send()
            return redirect('verify-email-done')
        else:
            return redirect('signup')
    
    context = {
        'user': request.user,
    }
    return render(request, 'users/authentication/verify_email.html', context=context)

def verify_email_done(request):
    user = request.user
    email = user.email
    context = {'user': user, 'email': email}
    return render(request, 'users/authentication/verify_email_done.html', context=context)

def verify_email_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.email_is_verified = True
        user.save()
        messages.success(request, 'Your email has been verified.')
        return redirect('verify-email-complete')   
    else:
        messages.warning(request, 'The link is invalid.')
    return render(request, 'users/authentication/verify_email_confirm.html')

def verify_email_complete(request):
    return render(request, 'users/authentication/verify_email_complete.html')

def change_email(request):
    user = request.user
    form = UserUpdateEmailForm()
    if request.method == 'POST':
        form = UserUpdateEmailForm(request.POST, instance=user)
        if form.is_valid():
            user.email = form.cleaned_data['email']
            user.save()
            return redirect('verify-email')
    
    context = {'form': form}
    return render(request, 'users/authentication/change_email.html', context=context)


# Create your views here.
def home_view(request):
    return render(request, 'users/home.html')



def login_view(request):
    # Logged in user can't register a new account
    if request.user.is_authenticated:
        return redirect("/")
    
    login_form = UserLoginForm(request.POST)
    

    if request.method == 'POST':
            login_form = UserLoginForm(request=request, data=request.POST)
            if login_form.is_valid():
                user = authenticate(
                    username=login_form.cleaned_data['username'],
                    password=login_form.cleaned_data['password'],
                )
                if user is not None:
                    login(request, user)
                    remember_me = login_form.cleaned_data.get('remember_me')
                    if not remember_me:
                        # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
                        request.session.set_expiry(0)
                    # Set session as modified to force data updates/cookie to be saved.
                    request.session.modified = True
                    if user.email_is_verified:
                        return redirect('dashboard')
                    else:
                        return redirect('verify-email')

                else:
                    for error in list(login_form.errors.values()):
                        messages.error(request, error)
            else:
                print("pas valide")
                
                    

       

    context = {
        'login_form': login_form,
       
    }

    return render(request, 'users/authentication/login.html', context=context)


def register_view(request):
    # Logged in user can't register a new account
    if request.user.is_authenticated:
        return redirect("/")
    
    register_form = UserRegistrationForm(request.POST)
    

    if request.method == 'POST':
        register_form = UserRegistrationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            password = register_form.cleaned_data['password2']
            user.set_password(password)
            user.username = user.email
            user.save()
            new_user = authenticate(username=user.email, password=password)
            login(request, new_user)
            return redirect('verify-email')
        else:
            for error in list(register_form.errors.values()):
                print(request, error)
    
    else:
        register_form = UserRegistrationForm()

    context = {
        'register_form': register_form,
    }

    return render(request, 'users/authentication/register.html', context=context)

@login_required
def custom_logout(request):
    logout(request)
    
    return render(request, "users/authentication/logout.html")

@login_required
def profile(request, slug):
    if request.method == 'POST':
        user = request.user
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user_form = form.save()

            messages.success(request, f'{user_form}, Your profile has been updated!')
            return redirect('profile', user_form.username)

        for error in list(form.errors.values()):
            messages.error(request, error)

    user = User.objects.filter(slug=slug).first()
    if user:
        form = UserUpdateForm(instance=user)
        return render(request, 'users/profile.html', context={'form': form})

    return redirect("home")