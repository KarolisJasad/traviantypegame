from django.contrib import admin
from .models import Village, Building, Resource
from django import forms
from django.db import connection

@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    list_display = ('name', 'player', 'population', 'granary_capacity', 'cranny_capacity')


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'village', 'b_type', 'level')


class ResourceAdminForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = '__all__'


class ResourceAdmin(admin.ModelAdmin):
    form = ResourceAdminForm
    list_display = ['village', 'r_type', 'generation_rate']

    def save_model(self, request, obj, form, change):
        # Check if the village has the corresponding building
        village = obj.village
        building_name = "Woodcutter"
        if Building.objects.filter(name=building_name, village=village).exists():
            super().save_model(request, obj, form, change)
        else:
            raise forms.ValidationError(f"The village does not have a {building_name} building.")

        # Save the resource instance
        
admin.site.register(Resource, ResourceAdmin)
