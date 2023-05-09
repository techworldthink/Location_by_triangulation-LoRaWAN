from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django .contrib.auth.models import User,auth
from django.conf import settings


def index(request):
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