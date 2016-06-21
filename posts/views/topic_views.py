import json, time

from django.db.models import Count, Max, F, Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

from userhub.models import User
from posts.models import Topic, Record, Tag


def topics_list(request):
    t0 = time.time()

    a, b, c, d = (set((q).values_list('topic', flat=True).distinct()) for q in
        [
            # is whitelist and not in whitelist
            Tag.objects.filter(access_mode=1),
            request.user.tag_set.filter(access_mode=1),
            # is blacklist and in blacklist
            Tag.objects.filter(access_mode=2),
            request.user.tag_set.filter(access_mode=2),
        ]
    )

    topics = (Topic.objects
        .exclude(id__in=(a-b)|(c&d))
        .annotate(last_post=Max('posts__created_at'))
        .order_by('-last_post')
        .select_related('author__profile')
        .prefetch_related('tags', 'posts')
    )[:20]

    t1 = time.time()

    last_seen = {r.topic_id: r.post_id for r in request.user.record_set.all()}

    for topic in topics:
        p, u = 0, 0
        for post in topic.posts.all():
            p += 1
            u += post.id > last_seen.get(topic.id, 0)
        topic.post_count = p
        topic.unseen_count = u

    t2 = time.time()
    sqlly = "{:.5f}s, {:.1f}% in python".format(t2-t0, 100-100*(t1-t0)/(t2-t0))
    context = {'topic_list': topics, 'sqlly_stuff': sqlly}
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

    ids = [int(s) for s in request.GET["ids"].split(',')]

    html_slugs = []
    for record in Record.objects.filter(user=request.user, topic_id__in=ids):
        topic = record.topic
        if record.topic.allows_access(request.user):
            topic.last_seen = record.post_id
            topic.unseen = topic.posts.filter(id__gt=topic.last_seen).count()
            html = render_to_string('posts/topic.html', {"topic": record.topic})
            html_slugs.append({"id": record.topic_id, "html": html})

    return JsonResponse(html_slugs, safe=False)
