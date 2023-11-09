from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model, authenticate
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control border-right-0', 'placeholder': _('Email')}),)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control border-right-0', 'placeholder': _('Username')}),)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control border-right-0', 'placeholder': _('Password'), 'data-toggle': 'password',}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control border-right-0', 'placeholder': _('Repeat Password'), 'data-toggle': 'password',}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class UserLoginForm(AuthenticationForm):

    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control border-right-0', 'placeholder': _('Email')}),)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control border-right-0', 'placeholder': _('Password'), 'data-toggle': 'password',}))
    remember_me = forms.BooleanField(required=False)

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username = username, password=password)
        if not user:
            if User.objects.filter(email=username).exists():
                message = _("This isn't the password registered with %(email)s. If you don't remember your password, please click on 'Forgot Password' .") % {'email':username}
                raise forms.ValidationError(message)
            else:
                message = _("No user registered with %(email)s...") % {'email': username}
                raise forms.ValidationError(message)
        
        
        return self.cleaned_data
    
    
    
    
class UserUpdateEmailForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control border-right-0', 'placeholder': _('Email')}),)
    class Meta:
        model = User
        fields = ['email']
    
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']