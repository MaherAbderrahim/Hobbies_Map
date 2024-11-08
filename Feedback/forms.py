from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['statut', 'description_feedback', 'url_images_feedback', 'need_admin']  # Les champs que vous souhaitez dans le formulaire
        widgets = {
            'description_feedback': forms.Textarea(attrs={'rows': 4, 'cols': 40}),  # Exemple de personnalisation pour le champ de texte
        }

    # Vous pouvez ajouter des méthodes de validation supplémentaires si nécessaire
    def clean_description_feedback(self):
        description = self.cleaned_data.get('description_feedback')
        if len(description) < 10:
            raise forms.ValidationError("La description doit comporter au moins 10 caractères.")
        return description
