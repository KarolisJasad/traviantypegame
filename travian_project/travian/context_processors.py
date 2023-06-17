from travian.models import Village
from .views import calculate_total_generation_rate

def village_context(request):
    village = None
    if request.user.is_authenticated:
        village = request.user.village.first()
    return {'village': village}

def generation_context(request):
    total_generation_rate = None
    if request.user.is_authenticated:
        village = Village.objects.get(user=request.user)
        total_generation_rate = calculate_total_generation_rate(village)
    return {'total_generation_rate': total_generation_rate}