from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect

from userhub.models import Profile

def login_view(request):
    if request.method == "GET":
        return render(request, 'userhub/login.html')

    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            context = {'error': 'disabled account'}
    else:
        context = {'error': 'invalid login'}
    return render(request, 'userhub/login.html', context)

@login_required(login_url='/login/')
def home_view(request):
    profile, is_new = Profile.objects.get_or_create(user=request.user)
    return render(request, 'userhub/home.html', {'profile': profile})

@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')
