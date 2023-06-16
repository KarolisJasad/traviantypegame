from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BuildingForm
from .models import Building, Resource, Village
from django.shortcuts import get_object_or_404
from django.db.models import F
from django.contrib import messages
from django.urls import reverse

def add_building(request):
    if request.method == 'POST':
        form = BuildingForm(request.POST)
        if form.is_valid():
            building = form.save()
            return redirect('travian/building_detail')
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
        elif deduct_resources(selected_building, village):
            add_building_and_resource(selected_building, village)
            messages.success(request, 'Building successfully constructed.')
        else:
            messages.error(request, 'Insufficient resources to build.')

        return redirect(reverse('build_building'))

    return render(request, 'travian/build_building.html', {'available_buildings': Building.objects.all()})

def upgrade_building(request):
    # Upgrade functionality
    village = get_object_or_404(Village, user=request.user)

    if request.method == 'POST':
        building_id = request.POST.get('building_id')
        selected_building = get_object_or_404(Building, id=building_id)
        # Check if the building is eligible for upgrade
        if selected_building.level >= 3:
            error_message = 'This building has reached its maximum level.'
            return render(request, 'travian/build_building.html', {'village_buildings': Building.objects.all(), 'error_message': error_message})

        village = get_object_or_404(Village, user=request.user)

        # Deduct resources for upgrade
        building_level = selected_building.level
        building_cost = selected_building.building_cost.get(str(building_level + 1), {})
        wood_cost = building_cost.get('wood', 0)
        clay_cost = building_cost.get('clay', 0)
        iron_cost = building_cost.get('iron', 0)
        crop_cost = building_cost.get('crop', 0)

        if village.wood_amount >= wood_cost and village.clay_amount >= clay_cost and village.iron_amount >= iron_cost and village.crop_amount >= crop_cost:
            # Update the village resource amounts
            Village.objects.filter(id=village.id).update(
                wood_amount=F('wood_amount') - wood_cost,
                clay_amount=F('clay_amount') - clay_cost,
                iron_amount=F('iron_amount') - iron_cost,
                crop_amount=F('crop_amount') - crop_cost
            )

            # Upgrade the selected building
            selected_building.level += 1
            selected_building.save()
        else:
            error_message = 'Insufficient resources.'
            return render(request, 'travian/build_building.html', {'available_buildings': Building.objects.all(), 'error_message': error_message})

    return render(request, 'travian/upgrade_building.html', {'village_buildings': village.building.all()})

def validate_building_constraints(building, village):
    if building.b_type == 'Resource':
        resource_name = building.name
        same_name_resources_count = village.resources.filter(building__name=resource_name).count()
        if same_name_resources_count >= 4:
            return 'You cannot have more than 4 buildings of the same type.'
    return None

def deduct_resources(building, village):
    building_level = building.level
    building_cost = building.building_cost.get(str(building_level), {})
    wood_cost = building_cost.get('wood', 0)
    clay_cost = building_cost.get('clay', 0)
    iron_cost = building_cost.get('iron', 0)
    crop_cost = building_cost.get('crop', 0)

    if (
        village.wood_amount >= wood_cost and
        village.clay_amount >= clay_cost and
        village.iron_amount >= iron_cost and
        village.crop_amount >= crop_cost
    ):
        Village.objects.filter(id=village.id).update(
            wood_amount=F('wood_amount') - wood_cost,
            clay_amount=F('clay_amount') - clay_cost,
            iron_amount=F('iron_amount') - iron_cost,
            crop_amount=F('crop_amount') - crop_cost
        )
        return True
    return False

def add_building_and_resource(building, village):
    village.building.add(building)
    resource_generation_rate = building.resource_generation_rate
    building_level = building.level
    generation_rate = resource_generation_rate.get(str(building_level), 0)
    resource = Resource.objects.create(village=village, generation_rate=generation_rate)
    resource.building.add(building)