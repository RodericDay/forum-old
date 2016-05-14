from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import urls as auth_urls
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def home(request):
    return render(request, 'home.html')

urlpatterns = [
    url(r'^$', home),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include(auth_urls)),
    url(r'^accounts/profile/$', home),
]
