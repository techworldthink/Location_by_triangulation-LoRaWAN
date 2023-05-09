from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test


@login_required()
@user_passes_test(lambda u: u.is_superuser)
def home(request):
    return render(request,"admin/home.html")