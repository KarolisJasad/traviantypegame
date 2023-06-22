from django import forms
from .models import Building, Village

class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = '__all__'

class VillageCreationForm(forms.ModelForm):
    class Meta:
        model = Village
        fields = ['name']
        labels = {'name': 'Village Name'}