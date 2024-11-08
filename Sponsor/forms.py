# forms.py
from django import forms
from .models import Sponsor

class SponsorForm(forms.ModelForm):
    class Meta:
        model = Sponsor
        fields = ['nom_sponsor', 'description_sponsor', 'prix_sponsor', 'url_site', 'url_photos', 'rentabilite_par_user']
