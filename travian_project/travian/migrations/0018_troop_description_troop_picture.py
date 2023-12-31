# Generated by Django 4.2.2 on 2023-06-22 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travian', '0017_alter_building_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='troop',
            name='description',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='troop',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='building_pictures', verbose_name='picture'),
        ),
    ]
