from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BuildingForm
from .models import Building, Resource, Village
from django.shortcuts import get_object_or_404

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
    user_id = request.user.id
    village = get_object_or_404(Village, user_id=user_id)

    if request.method == 'POST':
        building_id = request.POST.get('building_id')
        selected_building = get_object_or_404(Building, id=building_id)

        if selected_building.b_type == 'Resource':
            resource_name = selected_building.name
            same_name_resources_count = village.resources.filter(building__name=resource_name).count()
            if same_name_resources_count >= 4:
                error_message = 'You cannot have more than 4 buildings of the same type.'
                return render(request, 'travian/build_building.html', {'available_buildings': Building.objects.all(), 'error_message': error_message})

        village.building.add(selected_building)
        resource_generation_rate = selected_building.resource_generation_rate
        building_level = selected_building.level
        generation_rate = resource_generation_rate.get(str(building_level), 0)
        resource = Resource.objects.create(village=village, generation_rate=generation_rate)
        resource.building.add(selected_building)

    return render(request, 'travian/build_building.html', {'available_buildings': Building.objects.all()})