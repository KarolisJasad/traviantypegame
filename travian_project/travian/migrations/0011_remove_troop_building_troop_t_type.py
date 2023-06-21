# Generated by Django 4.2.2 on 2023-06-20 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travian', '0010_troop_construction_cost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='troop',
            name='building',
        ),
        migrations.AddField(
            model_name='troop',
            name='t_type',
            field=models.CharField(blank=True, choices=[('Infantry', 'Infantry'), ('Cavalry', 'Cavalry')], max_length=50, null=True, verbose_name='b_type'),
        ),
    ]