from django.contrib import admin
from .models import Village, Building, Resource
from django import forms
from django.db import connection

@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'population', 'granary_capacity', 'cranny_capacity', 'building_names')

    def building_names(self, obj):
        return ", ".join(building.name for building in obj.building.all())

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'b_type', 'level')

class ResourceAdminForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = '__all__'


class ResourceAdmin(admin.ModelAdmin):
    form = ResourceAdminForm
    list_display = ['village', 'building_names','generation_rate']

    def building_names(self, obj):
        return ", ".join(building.name for building in obj.building.all())
    

admin.site.register(Resource, ResourceAdmin)
