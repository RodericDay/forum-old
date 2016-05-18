from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

from posts.views.post_views import *
from posts.views.topic_views import *
from userhub.views import *

urlpatterns = [
    url(r'^$', topics_list),

    url(r'^topics/$', topics_list, name='topics-list'),
    url(r'^topics/new/$', topics_new, name='topics-new'),
    url(r'^topics/(\d+)/delete/$', topics_delete, name='topics-delete'),

    url(r'^topics/(\d+)/$', posts_list, name='posts-list'),
    url(r'^topics/(\d+)/new/$', posts_new, name='posts-new'),
    url(r'^topics/(\d+)/ajax/$', posts_ajax, name='posts-ajax'),

    url(r'^posts/(\d+)/edit/$', posts_edit, name='posts-edit'),
    url(r'^posts/(\d+)/delete/$', posts_delete, name='posts-delete'),

    url(r'^profile/$', home_view, name='profile'),
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^user-list/$', user_list_view, name='user-list'),
    url(r'^change-password/$', change_password_view, name='change-password'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
