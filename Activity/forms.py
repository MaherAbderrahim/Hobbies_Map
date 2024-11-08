from django import forms
from .models import Activity, Category
from Event.models import Event  # Assuming Event is defined in event/models.py

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = '__all__'  # Utilisez '__all__' pour inclure tous les champs

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
