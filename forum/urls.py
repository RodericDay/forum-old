from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

from posts.views.post_views import *
from posts.views.topic_views import *
from posts.views.tags_views import *
from userhub.views import *

urlpatterns = [
    url(r'^$', topics_list),

    url(r'^topics/$', topics_list, name='topics-list'),
    url(r'^topics/new/$', topics_new, name='topics-new'),
    url(r'^topics/ajax/$', topics_ajax, name='topics-ajax'),

    url(r'^topics/(\d+)/$', posts_list, name='posts-list'),
    url(r'^topics/(\d+)/reply/$', posts_reply, name='posts-reply'),
    url(r'^topics/(\d+)/ajax/$', posts_ajax, name='posts-ajax'),
    url(r'^topics/(\d+)/squash/(\d+)/$', posts_squash, name='posts-squash'),

    url(r'^posts/(\d+)/edit/$', posts_edit, name='posts-edit'),

    url(r'^tags/$', tags_list, name='tags-list'),
    url(r'^tags/(.+)/$', tags_edit, name='tags-edit'),
    url(r'^topics/(\d+)/tags/$', topic_tags_edit, name='topic-tags-edit'),

    url(r'^images/$', images_list, name='images-list'),
    url(r'^images/(\d+)/delete/$', images_delete, name='images-delete'),

    url(r'^profile/$', home_view, name='profile'),
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^users/$', user_list_view, name='user-list'),
    url(r'^change-password/$', change_password_view, name='change-password'),
    url(r'^todos/ajax/$', todos_ajax, name='todos-ajax'),

    url(r'^secret/', include(admin.site.urls)),
]
