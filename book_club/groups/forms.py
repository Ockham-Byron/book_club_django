from django import forms
from django.utils.translation import gettext_lazy as _
from .models import CustomGroup



class AddGroupForm(forms.ModelForm):
    
    name = forms.CharField(max_length=100, 
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': _("Group's Name"),
                                                            'class': 'form-control'
                                    }))
    
    
    class Meta:
        model = CustomGroup
        fields = ['name']