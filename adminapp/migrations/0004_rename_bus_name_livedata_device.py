# Generated by Django 4.1.7 on 2023-05-15 03:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0003_remove_livedata_device_name_livedata_bus_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='livedata',
            old_name='bus_name',
            new_name='device',
        ),
    ]
