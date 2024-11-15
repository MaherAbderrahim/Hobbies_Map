from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['statut', 'description_feedback', 'need_admin'] # Les champs que vous souhaitez dans le formulaire
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),  # Exemple de personnalisation pour le champ de texte
        }

    # Vous pouvez ajouter des méthodes de validation supplémentaires si nécessaire
    def clean_description_feedback(self):
        description_feedback = self.cleaned_data.get('description_feedback')
        if len(description_feedback) < 10:
            raise forms.ValidationError("La description doit comporter au moins 10 caractères.")
        return description_feedback
