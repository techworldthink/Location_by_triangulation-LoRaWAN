from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from .models import Chirpstack
from django .contrib import messages

@login_required()
@user_passes_test(lambda u: u.is_superuser)
def home(request):
    return render(request,"admin/home.html")


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