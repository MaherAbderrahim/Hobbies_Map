from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm

from .models import Utilisateur
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
#from .forms import CustomPasswordResetForm
from django.contrib.auth import get_user_model

class UtilisateurCreationForm(UserCreationForm):
    class Meta:
        model = Utilisateur
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Firstname'}),
            'last_name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Lastname'}),
            'email': forms.EmailInput(attrs={'class': 'input-field', 'placeholder': 'Email'}),
            'password1' : forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'Confirm Password'}),
        }

class UtilisateurLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'input-field', 'placeholder': 'Email'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'Password'})
    )

User = get_user_model() 

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'input-field', 'placeholder': 'Enter your email'})
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is not registered.")
        return email





