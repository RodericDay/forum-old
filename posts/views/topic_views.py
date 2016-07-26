import json, time

from django.core.paginator import Paginator
from django.db.models import *
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

from userhub.models import User
from posts.models import Topic, Record, Tag


PAGE_COUNT = 25

def get_topics(user, tag_name_list=None, topic_id_list=None, page=1):
    if tag_name_list:
        tags = Tag.objects.filter(name__in=tag_name_list)
        tag_ids = tags.values_list("topic", flat=True)
        All = Topic.objects.filter(id__in=tag_ids)
    else:
        All = Topic.objects

    w, b, wu, bu = (set(q.values_list('topic', flat=True)) for q in
        [
            Tag.objects.filter(access_mode=Tag.WHITELIST),
            Tag.objects.filter(access_mode=Tag.BLACKLIST),
            user.tag_set.filter(access_mode=Tag.WHITELIST),
            user.tag_set.filter(access_mode=Tag.BLACKLIST),
        ]
    )
    blocked = tuple((w-wu)|(b&bu))

    topics = (All
        .exclude(id__in=blocked)
        .annotate(last_update=Max('posts__created_at'))
        .annotate(post_count=Count('posts'))
        .order_by('-last_update')
    )

    if topic_id_list is None:  # pagination
        try:
            page = max(1, int(page))
        except:
            page = 1
        A, B = (page-1)*PAGE_COUNT, (page)*PAGE_COUNT
        topics = topics[A:B]

    topics = (topics
        .select_related('author__profile')
        .prefetch_related('tags', 'posts__author__profile')
    )
    topic_ids = topics.values_list("id", flat=True)

    records = {r.topic_id:r.post_id for r in Record.objects
        .filter(user=user, topic_id__in=topic_ids)
        .select_related('post')
    }

    for topic in topics:
        n = records.get(topic.id)
        if n:
            topic.unseen_count = sum(p.id > n for p in topic.posts.all())
        else:
            topic.unseen_count = topic.post_count
        topic.last_post = topic.posts.all()[:][-1]

    return topics


def topics_list(request):
    t0 = time.time()
    tags = request.GET.getlist("tag")
    page = request.GET.get("page")
    context = {
        'time_taken': time.time() - t0,
        'topic_list': get_topics(request.user, tags, page=page),
        'page_list': range(1, Topic.objects.all().count()//PAGE_COUNT+2),
    }
    return render(request, 'posts/topic_list.html', context)

def topics_new(request):
    context = {}
    if request.method == 'POST':
        topic_name = request.POST["name"]
        if len(topic_name) >= 5:
            content = request.POST.get("content", "")
            topic = Topic.objects.create(author=request.user, name=topic_name)
            topic.posts.create(author=request.user, content=content)
            return redirect(topic)
        else:
            context['error'] = "title must be at least 5 characters long"
    context['topic'] = {'name': request.POST.get("name", "")}
    context['post'] = {'content': request.POST.get("content", "")}
    return render(request, 'posts/topic_form.html', context)

def topics_ajax(request):
    if "ids" not in request.GET:
        return HttpResponse("")

    topic_id_list = [int(s) for s in request.GET.getlist("ids")]

    html_slugs = []
    for topic in get_topics(request.user, topic_id_list):
        html = render_to_string('posts/topic.html', {"topic": record.topic})
        html_slugs.append({"id": record.topic_id, "html": html})

    return JsonResponse(html_slugs, safe=False)
