# Generated by Django 4.2.2 on 2023-06-22 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travian', '0015_building_description_building_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='description',
            field=models.TextField(blank=True, max_length=300, null=True, verbose_name='description'),
        ),
    ]
