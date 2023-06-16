from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BuildingForm
from .models import Building, Resource, Village, VillageBuilding
from django.shortcuts import get_object_or_404
from django.db.models import F
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse

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
            if deduct_resources(selected_building, village, 1):
                existing_building = village.village_buildings.filter(building=selected_building).first()
                if existing_building:
                    # Get the count of existing buildings of the same type
                    existing_count = village.village_buildings.filter(building=selected_building).count()
                    # Generate the new name based on the count
                    new_name = f"{selected_building.name} {existing_count + 1}"
                    # Create a new VillageBuilding instance with the new name
                    village_building = VillageBuilding.objects.create(
                        village=village,
                        building=selected_building,
                        name=new_name
                    )
                    messages.success(request, 'Building successfully constructed.')
                else:
                    # Create a new VillageBuilding instance with the initial name
                    village_building = VillageBuilding.objects.create(
                        village=village,
                        building=selected_building,
                        name=selected_building.name
                    )
                    messages.success(request, 'Building successfully constructed.')
                add_building_and_resource(selected_building, village)
                messages.success(request, 'Building successfully constructed.')
            else:
                messages.error(request, 'Insufficient resources to build.')

        return redirect(reverse('build_building'))

    return render(request, 'travian/build_building.html', {'available_buildings': Building.objects.all()})

@login_required
def upgrade_building(request):
    if request.method == 'POST':
        building_id = request.POST.get('building_select')
        if building_id:
            village_building = get_object_or_404(VillageBuilding, id=building_id)
            selected_building = village_building.building
            village = village_building.village

            # Check if the player has enough resources for the upgrade
            if has_enough_resources(selected_building, village, village_building.level):
                # Deduct the resources for the upgrade
                deduct_resources(selected_building, village, village_building.level)

                # Upgrade the building level
                village_building.level += 1
                village_building.save()

                return HttpResponse(f"Building with ID {building_id} has been upgraded to level {village_building.level}.")
            else:
                return HttpResponse("Insufficient resources to upgrade the building.")

    return render(request, 'travian/upgrade_building.html')

def generate_building_name(building, village):
    # Get the count of existing buildings of the same type in the village
    existing_building_count = village.village_buildings.filter(building=building).count()

    # Generate the new name by appending the count to the building name
    new_name = f"{building.name} {existing_building_count + 1}"

    return new_name

def validate_building_constraints(building, village):
    if building.b_type == 'Resource':
        resource_name = building.name
        same_name_resources_count = village.resources.filter(building__name=resource_name).count()
        if same_name_resources_count >= 4:
            return 'You cannot have more than 4 buildings of the same type.'
    return None

def has_enough_resources(building, village, current_level):
    building_cost = building.building_cost.get(str(current_level + 1))
    if building_cost:
        wood_cost = building_cost.get('wood', 0)
        clay_cost = building_cost.get('clay', 0)
        iron_cost = building_cost.get('iron', 0)
        crop_cost = building_cost.get('crop', 0)

        return (
            village.wood_amount >= wood_cost and
            village.clay_amount >= clay_cost and
            village.iron_amount >= iron_cost and
            village.crop_amount >= crop_cost
        )
    return False

def deduct_resources(building, village, current_level=0):
    building_cost = building.building_cost.get(str(current_level))
    if building_cost:
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