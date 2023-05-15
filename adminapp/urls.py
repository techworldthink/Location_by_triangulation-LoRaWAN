
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('chirpstack',views.chirpstack,name='chirpstack'),
    path('device',views.device,name='device'),
    path('bus_stops',views.bus_stops,name='bus_stops'), 
    path('dashboard',views.dashboard,name='dashboard'),
    path('device/delete/<int:id>/',views.device_delete,name='device_delete'),
]
