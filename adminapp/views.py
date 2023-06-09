from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django .contrib import messages
from django.http import JsonResponse
import json

from .models import Chirpstack
from .models import DeviceEui
from .models import BusStops



@login_required()
@user_passes_test(lambda u: u.is_superuser)
def home(request):
    return render(request,"admin/home.html")


@login_required()
@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):
    return render(request,"admin/dashboard.html")

@login_required()
@user_passes_test(lambda u: u.is_superuser)
def chirpstack(request):
    chirpstack_config = Chirpstack.objects.first()

    if request.method == 'POST':
        # Clear any existing Chirpstack configurations
        Chirpstack.objects.all().delete()
        chirpstack_config = Chirpstack.objects.create(
            server_url=request.POST.get('chirp_url'),
            user_name=request.POST.get('chirp_user'),
            password=request.POST.get('chirp_pass'),
        )
        messages.success(request, "Server configuration successfully updated.")

    context = {
        'chirpstack_config': chirpstack_config,
    }

    return render(request, "admin/chirpstack.html", context)


@login_required()
@user_passes_test(lambda u: u.is_superuser)
def device(request):
    if request.method == 'POST':
        chirpstack_config = DeviceEui.objects.create(
            bus_name=request.POST.get('bus_name'),
            device_eui=request.POST.get('deveui'),
        )
        messages.success(request, "Device added")
    
    context = {
        "devices" : DeviceEui.objects.filter()
    }

    return render(request, "admin/device.html",context)


@login_required()
@user_passes_test(lambda u: u.is_superuser)
def device_delete(request,id):
    try:
        device_obj = DeviceEui.objects.get(id=id)
        device_obj.delete()
        messages.success(request, "Device deleted")
    except:
        messages.success(request, "Device deletion failed")
    
    return redirect('device')

@login_required()
@user_passes_test(lambda u: u.is_superuser)
def bus_stops(request):
    if request.method == 'POST':
        stop_name = BusStops.objects.create(
            stop_name=request.POST.get('stop_name'),
            latitude=request.POST.get('lat'),
            longitude=request.POST.get('lon'),
        )
        return JsonResponse({'status':'ok'})
    bus_stops = BusStops.objects.filter().values()
    context = {
        'stops' : json.dumps(list(bus_stops), indent=4, sort_keys=True, default=str),
        'bus_stops' : bus_stops
    }
    return render(request, "admin/bus_stops.html",context)


@login_required()
@user_passes_test(lambda u: u.is_superuser)
def bus_stop_delete(request,id):
    try:
        bus_stop_obj = BusStops.objects.get(id=id)
        bus_stop_obj.delete()
        messages.success(request, "Bus stops deleted")
    except:
        messages.success(request, "Bus stop deletion failed")
    return redirect('bus_stops')