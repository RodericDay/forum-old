import pytz

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden

from userhub.models import User, Profile, Image


def login_view(request):
    if request.method == "GET":
        return render(request, 'userhub/login.html')

    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect("/profile/")
        else:
            context = {'error': 'disabled account'}
    else:
        context = {'error': 'invalid login'}
    return render(request, 'userhub/login.html', context)

def home_view(request):
    profile = request.user.profile

    if request.method == "POST":
        tz = request.POST.get("timezone")
        new_avatar = request.FILES.get("avatar")
        if new_avatar:
            profile.avatar = new_avatar
        if tz in pytz.common_timezones:
            profile.timezone = tz
        profile.save()
        return HttpResponseRedirect('/profile/')

    context = {
        'profile': profile,
        'timezones': pytz.common_timezones,
    }
    return render(request, 'userhub/home.html', context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')

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

def user_list_view(request):
    context = {}
    if request.user.is_superuser and request.method == "POST":
        username = request.POST["new_username"]
        if username:
            user = User.objects.create(username=username)
            user.set_password("password")
            user.save()
    context["user_list"] = User.objects.all().order_by("username")
    for user in context["user_list"]:
        ts = [r.post.modified_at for r in user.record_set.all() if r.post_id]
        if ts:
            user.last_record = max(ts)
    return render(request, 'userhub/user_list.html', context)

def images_list(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    context = {'image_list': Image.objects.all()}
    if request.method == "POST":
        raw = request.FILES.get("raw")
        if raw:
            Image.objects.create(raw=raw, uploader=request.user)
        return HttpResponseRedirect('/images/')
    return render(request, 'userhub/images.html', context)

def images_delete(request, image_id):
    if request.user.is_superuser and request.method == "POST":
        image = get_object_or_404(Image, id=image_id)
        image.full_delete()
        return HttpResponseRedirect('/images/')
    return HttpResponseForbidden()
