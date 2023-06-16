# Generated by Django 4.2.2 on 2023-06-16 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travian', '0002_village_building'),
    ]

    operations = [
        migrations.AlterField(
            model_name='village',
            name='building',
            field=models.ManyToManyField(blank=True, related_name='buildings', through='travian.VillageBuilding', to='travian.building', verbose_name='buildings'),
        ),
    ]
