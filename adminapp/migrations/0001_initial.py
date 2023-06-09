# Generated by Django 4.1.7 on 2023-05-09 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusStops',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stop_name', models.CharField(max_length=100)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='Chirpstack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_url', models.CharField(max_length=100)),
                ('user_name', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DeviceEui',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bus_name', models.CharField(max_length=100)),
                ('device_eui', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='LiveData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_name', models.CharField(max_length=100)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('co2', models.DecimalField(decimal_places=5, max_digits=9)),
                ('iaq', models.DecimalField(decimal_places=5, max_digits=9)),
                ('bvoc', models.DecimalField(decimal_places=5, max_digits=9)),
                ('temperature', models.DecimalField(decimal_places=5, max_digits=9)),
                ('humidity', models.DecimalField(decimal_places=5, max_digits=9)),
                ('pressure', models.DecimalField(decimal_places=5, max_digits=9)),
            ],
        ),
    ]
