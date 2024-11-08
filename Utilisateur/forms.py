from django import forms
from .models import User

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nom_user', 'prenom_user', 'email_user', 'is_premium_user']  # Ajoute les champs nécessaires

    def save(self, commit=True):
        user = super().save(commit=False)
        print(user)
        user.set_password(self.cleaned_data['password'])  # Hash le mot de passe
        if commit:
            user.save()
        return user
