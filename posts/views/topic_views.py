from django.db.models import Max, F
from django.http import HttpResponseRedirect
from django.shortcuts import render

from posts.models import Topic


def topics_list(request):
    topics = Topic.objects.annotate(last_post=Max('posts__created_at'))
    context = {'topic_list': topics.order_by('-last_post')}
    return render(request, 'posts/topic_list.html', context)

def topics_new(request):
    context = {}
    if request.method == 'POST':
        topic_name = request.POST["name"]
        if len(topic_name) > 5:
            content = request.POST.get("content", "")
            topic = Topic.objects.create(author=request.user, name=topic_name)
            topic.posts.create(author=request.user, content=content)
            return HttpResponseRedirect('/topics/')
        else:
            context['error'] = "title must be at least 5 characters long"
    context['topic'] = {'name': request.POST.get("name", "")}
    context['post'] = {'content': request.POST.get("content", "")}
    return render(request, 'posts/topic_form.html', context)

def topics_delete(request):
    return HttpResponseRedirect("/")

def topics_ajax(request):
    return HttpResponseRedirect("/")
