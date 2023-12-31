from celery import shared_task
from .utils_tasks import calculate_total_generation_rate
from django.db.models import F


@shared_task
def update_resource_amount():
    from .models import Village
    print("Labas")
    villages = Village.objects.all()
    for village in villages:
        total_generation_rate = calculate_total_generation_rate(village)
        print(total_generation_rate.get('Crop', 0))
        if village.wood_amount < village.warehouse_capacity:
            village.wood_amount = F('wood_amount') + total_generation_rate.get('Woodcutter', 0) / 1800
        else:
            village.wood_amount = village.warehouse_capacity
        if village.clay_amount < village.warehouse_capacity:
            village.clay_amount = F('clay_amount') + total_generation_rate.get('Clay_pit', 0) / 1800
        else:
            village.clay_amount = village.warehouse_capacity
        if village.iron_amount < village.warehouse_capacity:
            village.iron_amount = F('iron_amount') + total_generation_rate.get('Iron_mine', 0) / 1800
        else:
            village.iron_amount = village.warehouse_capacity
        if total_generation_rate.get('Crop', 0) <= 0:
            village.crop_amount = F('crop_amount') - total_generation_rate.get('Crop', 0) / 1800
        else:
            if village.crop_amount < village.granary_capacity:
                village.crop_amount = F('crop_amount') + total_generation_rate.get('Crop', 0) / 1800
            else:
                village.crop_amount = village.granary_capacity
        village.save()
