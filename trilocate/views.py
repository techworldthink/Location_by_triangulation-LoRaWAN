from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django .contrib.auth.models import User,auth
from django.conf import settings
from django.db.models import Max
from adminapp.models import LiveData
from shedulerapp.tasks import activate_live_frame_analysis
import json


def index(request):
    activate_live_frame_analysis()
    return render(request,"home/index.html") 

def login(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request,user)
            if user.is_superuser:
                settings.LOGIN_REDIRECT_URL = '/admin/'
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            message = 'Invalid login credentials'
    else:
        message = ''
    return render(request,"home/login.html", {'message': message}) 


# logout
@login_required()
@user_passes_test(lambda u: u.is_staff)
def logout(request):
    auth.logout(request)
    return redirect("/")

# public live map
def live_map(request):
    last_data_per_bus_stop = LiveData.objects.values('bus_stop').annotate(
        max_live_time=Max('live_time')).order_by()

    last_data = LiveData.objects.filter(
        bus_stop__in=last_data_per_bus_stop.values('bus_stop'),
        live_time__in=last_data_per_bus_stop.values('max_live_time')
    ).values()

    map_data = json.dumps(list(last_data), indent=4, sort_keys=True, default=str)
    #
    context = {
        "map_data" : map_data
    }
    return render(request,"home/live_map.html",context) 




