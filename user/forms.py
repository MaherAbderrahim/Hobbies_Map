from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Utilisateur

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
