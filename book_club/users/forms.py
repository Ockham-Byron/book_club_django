from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model, authenticate
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import PrependedText
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model



class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control border-right-0', 'placeholder': _('Email')}),)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control border-right-0', 'placeholder': _('Username')}),)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control border-right-0', 'placeholder': _('Password')}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control border-right-0', 'placeholder': _('Repeat Password')}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class UserLoginForm(AuthenticationForm):

    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control border-right-0', 'placeholder': _('Email')}),)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control border-right-0', 'placeholder': _('Password')}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username = username, password=password)
        if not user:
            if get_user_model().objects.filter(email=username).exists():
                message = _("This isn't the password registered with %(email)s. If you don't remember your password, please click on 'Forgot Password' .") % {'email':username}
                raise forms.ValidationError(message)
            else:
                message = _("No user registered with %(email)s...") % {'email': username}
                raise forms.ValidationError(message)
        
        
        return self.cleaned_data
    
    
    
    

    
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']