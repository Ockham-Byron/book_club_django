from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserLoginForm, UserUpdateForm

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from .tokens import account_activation_token

def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')
...

# Create your views here.
def home_view(request):
    return render(request, 'users/home.html')

def auth_view(request):
    # Logged in user can't register a new account
    if request.user.is_authenticated:
        return redirect("/")
    
    login_form = UserLoginForm(request.POST)
    register_form = UserRegistrationForm(request.POST)

    if request.method == 'POST':
        if 'login_form' in request.POST:
            print("Login form")
            login_form = UserLoginForm(request=request, data=request.POST)
            if login_form.is_valid():
                user = authenticate(
                    username=login_form.cleaned_data['username'],
                    password=login_form.cleaned_data['password'],
                )
                if user is not None:
                    print("user reconnu")
                    login(request, user)
                    message = _('Hello %(username) ! You have been logged in !.') % {'username':user.username}
                    messages.success(request, message)
                    return redirect('home')

                else:
                    for error in list(login_form.errors.values()):
                        messages.error(request, error)
            else:
                print("pas valide")
                if get_user_model().objects.filter(email = login_form.cleaned_data['username']).exists():
                    print("pas bon mot de passe")
                    message = _("This isn't the password connected with this %(email)") % {'email':login_form.cleaned_data['username']}
                    raise ValidationError(request, message)
                else:
                    print("pas usernames")
                    message = _("No user registered with this %(email)...") % {'email':login_form.cleaned_data['username']}
                    messages.error(request, message)
                    

        if 'register_form' in request.POST:
            register_form = UserRegistrationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save(commit=False)
                user.is_active = False
                user.save()
                activateEmail(request, user, register_form.cleaned_data.get('email'))
                return redirect('/')
            else:
                for error in list(register_form.errors.values()):
                    print(request, error)
        else:
            register_form = UserRegistrationForm()

    context = {
        'login_form': login_form,
        'register_form': register_form,
    }

    return render(request, 'users/authentication/authentication.html', context=context)



@login_required
def custom_logout(request):
    logout(request)
    
    return redirect("home")

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

    user = get_user_model().objects.filter(slug=slug).first()
    if user:
        form = UserUpdateForm(instance=user)
        return render(request, 'users/profile.html', context={'form': form})

    return redirect("home")