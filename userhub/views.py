from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect

from userhub.models import User, Profile

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

    if request.method == "POST":
        new_avatar = request.FILES.get("avatar")
        if new_avatar:
            profile.avatar = new_avatar
            profile.save()

    return render(request, 'userhub/home.html', {'profile': profile})

@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')

@login_required(login_url='/login/')
def change_password_view(request):
    context = {}
    if request.method == "POST":
        try:
            if not request.user.check_password(request.POST["old"]):
                raise ValueError("Old password incorrect")
            if request.POST["new1"] != request.POST["new2"]:
                raise ValueError("New pair does not match")
            raw_password = request.POST["new1"]
            if raw_password == "":
                raise ValueError("Password needs to be somewhat decent...")
            request.user.set_password(raw_password)
            request.user.save()
            return HttpResponseRedirect("/logout/")
        except ValueError as e:
            context["error"] = e
    return render(request, 'userhub/change_password_form.html', context)

@login_required(login_url='/login/')
def user_list_view(request):
    context = {}
    if request.method == "POST":
        username = request.POST["new_username"]
        if username:
            user = User.objects.create(username=username)
            user.set_password("password")
            user.save()
    context["user_list"] = User.objects.all()
    return render(request, 'userhub/user_list.html', context)
