from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import BuildingForm
from collections import defaultdict
from .models import Building, Resource, Village, VillageBuilding
from django.db.models import F
from django.http import HttpResponse
from .utils import *
from .utils_views import *


def add_building(request):
    if request.method == 'POST':
        form = BuildingForm(request.POST)
        if form.is_valid():
            building = form.save()
            return redirect(reverse('add_building'))
    else:
        form = BuildingForm()
    return render(request, 'travian/add_building.html', {'form': form})


def base(request):
    return render(request, 'base.html')


@login_required
def build_building(request):
    if request.method == 'POST':
        building_id = request.POST.get('building_id')
        selected_building = get_object_or_404(Building, id=building_id)
        village = get_object_or_404(Village, user=request.user)
        error_message = validate_building_constraints(selected_building, village)

        if error_message:
            messages.error(request, error_message)
        else:
            if check_and_deduct_resources(selected_building, village, 0):
                existing_building_count = village.village_buildings.filter(building=selected_building).count()
                new_name = generate_building_name(selected_building, existing_building_count + 1)
                resource = create_resource(selected_building, village)
                create_village_building(village, selected_building, resource, new_name)
                update_population(village)
                messages.success(request, 'Building successfully constructed.')
            else:
                messages.error(request, 'Insufficient resources to build.')

        return redirect(reverse('build_resource'))

    return render(request, 'travian/build_resource.html', {'available_buildings': Building.objects.all()})

@login_required
def build_infrastructure(request):
    if request.method == 'POST':
        building_id = request.POST.get('building_id')
        selected_building = get_object_or_404(Building, id=building_id)
        village = get_object_or_404(Village, user=request.user)

        if village.village_buildings.filter(building=selected_building).exists():
            messages.error(request, f"You already have a {selected_building.name}. You cannot build another one.")
        else:
            if check_and_deduct_resources(selected_building, village, 0):
                village_building = create_village_infrastructure(village, selected_building, name=selected_building.name)
                update_population(village)
                update_village_resource_capacity(selected_building, village_building)  # Updated this line
                messages.success(request, 'Building successfully constructed.')
            else:
                messages.error(request, 'Insufficient resources to build.')

        return redirect(reverse('build_infrastructure'))

    available_buildings = Building.objects.filter(b_type='Infrastructure')
    return render(request, 'travian/build_infrastructure.html', {'available_buildings': available_buildings})

@login_required
def upgrade_building(request):
    if request.method == 'POST':
        building_id = request.POST.get('building_select')
        if building_id:
            village_building = get_object_or_404(VillageBuilding, id=building_id)
            selected_building = village_building.building
            village = village_building.village
            current_level = village_building.level

            if current_level >= 10:
                messages.error(request, 'Building is already at its maximum level.')
            elif check_and_deduct_resources(selected_building, village, current_level):
                new_level = upgrade_building_level(village_building)

                if selected_building.b_type == 'Resource':
                    update_resource_generation_rate(village_building)
                elif selected_building.name in ('Granary', 'Warehouse'):
                    update_village_resource_capacity(selected_building, village_building)

                update_population(village)
                messages.success(request, 'Building successfully upgraded.')
            else:
                messages.error(request, 'Insufficient resources to upgrade.')

    return render(request, 'travian/upgrade_building.html', {'messages': messages.get_messages(request)})

def generate_building_name(building, count):
    return f"{building.name} {count}"
