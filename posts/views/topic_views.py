from django.db.models import Max
from django.http import HttpResponseRedirect
from django.shortcuts import render

from posts.models import Topic


def topics_list(request):
    topics = Topic.objects.annotate(last_post=Max('posts__created_at'))
    ordered = topics.order_by('-last_post')
    visible = [topic for topic in ordered if topic.allows_access(request.user)]
    context = {'topic_list': visible}
    return render(request, 'posts/topic_list.html', context)

def topics_new(request):
    context = {}
    if request.method == 'POST':
        topic_name = request.POST["name"]
        if len(topic_name) >= 5:
            content = request.POST.get("content", "")
            topic = Topic.objects.create(author=request.user, name=topic_name)
            topic.posts.create(author=request.user, content=content)
            return HttpResponseRedirect(topic.get_absolute_url())
        else:
            context['error'] = "title must be at least 5 characters long"
    context['topic'] = {'name': request.POST.get("name", "")}
    context['post'] = {'content': request.POST.get("content", "")}
    return render(request, 'posts/topic_form.html', context)

def topics_delete(request):
    return HttpResponseRedirect("/")

def topics_ajax(request):
    return HttpResponseRedirect("/")
