from datetime import timedelta
from celery import shared_task
from django.db.models import F
from travian.models import Resource, Village
from travian_project.celery import app
from .utils import calculate_total_generation_rate

@shared_task
def update_resource_amount():
    print("Labas")
    villages = Village.objects.all()
    for village in villages:
        total_generation_rate = calculate_total_generation_rate(village)

        village.wood_amount = F('wood_amount') + total_generation_rate.get('Woodcutter', 0) / 60
        village.clay_amount = F('clay_amount') + total_generation_rate.get('Clay_pit', 0) / 60
        village.iron_amount = F('iron_amount') + total_generation_rate.get('Iron_mine', 0) / 60
        village.crop_amount = F('crop_amount') + total_generation_rate.get('Crop', 0) / 60

        village.save()


@shared_task(bind=True)
def test_func(self):
    #operations
    for i in range(10):
        print(i)
    return "Done"