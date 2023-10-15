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
    device = models.ForeignKey(DeviceEui, on_delete=models.CASCADE,default=None, null=True)
    bus_stop = models.ForeignKey(BusStops, on_delete=models.CASCADE,default=None, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    co2 = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    iaq = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    bvoc = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    temperature = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    humidity = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    pressure = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    live_time = models.DateTimeField(default=timezone.now, null=True)
    device_eui = models.CharField(max_length=30, null=True)
    frame_count = models.IntegerField(blank=True, null=True)


