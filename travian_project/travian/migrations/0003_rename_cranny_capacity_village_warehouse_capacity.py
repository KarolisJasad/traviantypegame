# Generated by Django 4.2.2 on 2023-06-19 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travian', '0002_alter_village_clay_amount_alter_village_crop_amount_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='village',
            old_name='cranny_capacity',
            new_name='warehouse_capacity',
        ),
    ]