import re

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from posts.models import Tag, Topic

def tags_list(request):
    context = {'tag_list': Tag.objects.all()}
    if request.method == "POST" and request.user.is_superuser:
        name = request.POST["name"]
        if name:
            Tag.objects.create(name=name)
        return HttpResponseRedirect('/tags/')
    return render(request, 'posts/tags_list.html', context)

def tags_edit(request, name):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/topics/')
    tag = Tag.objects.get(name=name)
    if request.user.is_superuser and request.method == "POST":
        tag.name = request.POST['name']
        tag.access_mode = request.POST['access_mode']
        tag.access_list = User.objects.filter(id__in=request.POST.getlist('access_list'))
        tag.save()
        return HttpResponseRedirect(tag.get_absolute_url())
    context = {
        'tag': tag,
        'user_list': User.objects.all(),
    }
    return render(request, 'posts/tags_form.html', context)

def topic_tags_edit(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method == "POST":
        strings = re.findall(r'\w+', request.POST["tags_as_string"])
        tags = Tag.objects.filter(name__in=strings)
        topic.tags = tags[:5]
        topic.save()
    return HttpResponseRedirect(topic.get_absolute_url())
