# Generated by Django 4.2.2 on 2023-06-19 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travian', '0003_rename_cranny_capacity_village_warehouse_capacity'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='extra_attributes',
            field=models.JSONField(blank=True, null=True, verbose_name='extra_attributes'),
        ),
    ]