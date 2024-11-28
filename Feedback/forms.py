from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['status', 'feedback_type', 'description_feedback', 'need_admin','rating']
        widgets = {
            'description_feedback': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Please describe your feedback'}),
            'rating': forms.Select(choices=[(i, f"{i} ★") for i in range(1, 6)]),  # Dropdown with stars

        }
        

    # Vous pouvez ajouter des méthodes de validation supplémentaires si nécessaire
    def clean_description_feedback(self):
        description_feedback = self.cleaned_data.get('description_feedback')
        if len(description_feedback) < 10:
            raise forms.ValidationError("La description doit comporter au moins 10 caractères.")
        return description_feedback
