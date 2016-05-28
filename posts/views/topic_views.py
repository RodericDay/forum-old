import json

from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string

from posts.models import Topic, Record


def topics_list(request):
    topics = Topic.objects.annotate(last_post=Max('posts__created_at'))
    ordered = topics.order_by('-last_post')
    if 'tags' in request.GET:
        ordered = ordered.filter(tags__name=request.GET['tags'])
    visible = [topic for topic in ordered if topic.allows_access(request.user)]
    records = {record.topic_id: record.post_id for record
                in Record.objects.filter(user=request.user)}

    for topic in visible:
        topic.last_seen = 0
        topic.unseen = 0
        if topic.id in records:
            topic.last_seen = records[topic.id]
            topic.unseen = topic.posts.filter(id__gt=topic.last_seen).count()

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
    if "ids" not in request.GET:
        return HttpResponse("")

    ids = [int(s) for s in request.GET["ids"].split(',')]

    html_slugs = []
    for record in Record.objects.filter(user=request.user, topic_id__in=ids):
        topic = record.topic
        if record.topic.allows_access(request.user):
            topic.last_seen = record.post_id
            topic.unseen = topic.posts.filter(id__gt=topic.last_seen).count()
            html = render_to_string('posts/topic.html', {"topic": record.topic})
            html_slugs.append({"id": record.topic_id, "html": html})

    string = json.dumps(html_slugs)
    return HttpResponse(string)
