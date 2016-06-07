from django.contrib import admin

from posts.models import Topic


class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    fields = ('name', 'author')

admin.site.register(Topic, TopicAdmin)
