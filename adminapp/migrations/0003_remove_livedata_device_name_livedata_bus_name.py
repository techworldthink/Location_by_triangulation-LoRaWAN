# Generated by Django 4.1.7 on 2023-05-11 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0002_livedata_bus_stop_livedata_live_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='livedata',
            name='device_name',
        ),
        migrations.AddField(
            model_name='livedata',
            name='bus_name',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='adminapp.deviceeui'),
        ),
    ]
