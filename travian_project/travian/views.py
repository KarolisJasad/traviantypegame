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
            return redirect('building_detail', pk=building.pk)
    else:
        form = BuildingForm()
    return render(request, 'travian/add_building.html', {'form': form})

def base(request):
    return render(request, 'base.html')

@login_required
def build_building(request):
    available_buildings = Building.objects.all()
    user_id = request.user.id
    village = Village.objects.filter(user_id=user_id).first()
    village_id = village.id if village else None
    print(village_id)
    print(available_buildings)

    if request.method == 'POST':
        building_id = request.POST.get('building_id')
        try:
            selected_building = Building.objects.get(id=building_id)
        except Building.DoesNotExist:
            selected_building = None
        if selected_building and village_id:
            village = get_object_or_404(Village, id=village_id)
            village.building.add(selected_building)
            resource_generation_rate = selected_building.resource_generation_rate
            building_level = selected_building.level
            generation_rate = resource_generation_rate.get(str(building_level), 0)
            resource = Resource.objects.create(village=village, generation_rate=generation_rate)
            resource.building.add(selected_building)
            return render(request, 'travian/build_building.html', {'available_buildings': available_buildings})

    context = {
        'available_buildings': available_buildings,
        'village_id': village_id,
    }
    return render(request, 'travian/build_building.html', context)