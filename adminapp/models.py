from django.utils import timezone
from django.db import models


class Chirpstack(models.Model):
    server_url = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class DeviceEui(models.Model):
    bus_name = models.CharField(max_length=100)
    device_eui = models.CharField(max_length=30)

class BusStops(models.Model):
    stop_name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

class LiveData(models.Model):
    bus_name = models.ForeignKey(DeviceEui, on_delete=models.CASCADE,default=None)
    bus_stop = models.ForeignKey(BusStops, on_delete=models.CASCADE,default=None)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    co2 = models.DecimalField(max_digits=9, decimal_places=5)
    iaq = models.DecimalField(max_digits=9, decimal_places=5)
    bvoc = models.DecimalField(max_digits=9, decimal_places=5)
    temperature = models.DecimalField(max_digits=9, decimal_places=5)
    humidity = models.DecimalField(max_digits=9, decimal_places=5)
    pressure = models.DecimalField(max_digits=9, decimal_places=5)
    live_time = models.DateTimeField(default=timezone.now)

