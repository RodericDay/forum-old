from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

from userhub.views import *

urlpatterns = [
    url(r'^$', home_view, name='home'),
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
