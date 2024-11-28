from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'  # Include all fields from the Event model
        widgets = {
            'date_event': forms.DateInput(attrs={'type': 'date'}),  # Use a date picker widget
        }
