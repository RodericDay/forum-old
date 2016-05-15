from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

from posts.views import *
from userhub.views import *

urlpatterns = [
    url(r'^$', posts_view, name='posts'),
    url(r'^new/$', posts_new, name='new'),
    url(r'^edit/(\d+)$', posts_edit, name='edit'),
    url(r'^delete/(\d+)$', posts_delete, name='delete'),
    url(r'^profile/$', home_view, name='profile'),
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^change_password/$', change_password_view, name='change_password'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
