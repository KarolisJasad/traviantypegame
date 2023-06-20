from django.contrib import admin
from .models import Village, Building, Resource, Troop, VillageBuilding, VillageTroop

@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'population', 'warehouse_capacity', 'granary_capacity', 'building_names')

    def building_names(self, obj):
        return ", ".join(building.name for building in obj.building.all())

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'b_type', 'level')

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['village', 'building_names', 'generation_rate']

    def building_names(self, obj):
        return ", ".join(building.name for building in obj.building.all())

@admin.register(Troop)
class TroopAdmin(admin.ModelAdmin):
    list_display = ['t_type', 'name', 'attack', 'defense', 'carrying_capacity', 'construction_cost', 'crop_consumption']

@admin.register(VillageBuilding)
class VillageBuildingAdmin(admin.ModelAdmin):
    list_display = ['village', 'building', 'resource', 'name', 'level']

@admin.register(VillageTroop)
class VillageTroopAdmin(admin.ModelAdmin):
    list_display = ['village', 'troop', 'quantity']