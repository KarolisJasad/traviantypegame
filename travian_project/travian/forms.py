from django import forms
from .models import Village

class VillageCreationForm(forms.ModelForm):
    class Meta:
        model = Village
        fields = ['name']
        labels = {'name': 'Village Name'}