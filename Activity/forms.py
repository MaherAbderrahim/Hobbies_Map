from django import forms
from .models import Activity, Category # Ensure ActivityImage is imported

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = '__all__'
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

