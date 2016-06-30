from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone

from posts.models import Post, Topic, Tag, Record


def posts_list(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if not topic.allows_access(request.user):
        return HttpResponseForbidden()

    posts = topic.posts.all()
    Record.new(post=posts.last(), user=request.user, topic=topic)
    context = {"topic": topic, "post_list": posts}

    return render(request, 'posts/post_list.html', context)

def posts_reply(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if not topic.allows_access(request.user):
        return HttpResponseForbidden()

    if request.method == "POST":
        post = topic.posts.create(author=request.user, content=request.POST['content'])
        url = topic.get_absolute_url() + "#" + str(post.id)
        return redirect(url)

    context = {'topic_list': [topic]}
    return render(request, 'posts/post_detail.html', context)

def posts_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if not post.allows_access(request.user):
        return HttpResponseForbidden()

    context = {'action': 'edit', 'post': post}
    if request.method == "POST":

        if "delete" in request.POST:
            post.content = "[deleted]"
        else:
            post.content = request.POST['content']

        post.save()
        return redirect(post)

    context['topic_list'] = post.topic_set.all()
    return render(request, 'posts/post_detail.html', context)

def posts_squash(request, topic_id, post_id):
    topic = get_object_or_404(Topic, id=topic_id)
    all_posts = topic.posts.filter(id__lte=post_id).order_by("-created_at")
    tail_post, head_post = all_posts[:2]
    if head_post.author == tail_post.author:
        if request.user == head_post.author or request.user.is_superuser:
            head_post.content += '\n\n' + tail_post.content
            head_post.save()
            tail_post.delete()
    url = topic.get_absolute_url() + "#" + str(head_post.id)
    return redirect(url)

def get_posts(topic, user, timestamp, content=None):
    if not topic.allows_access(user):
        return []

    tail = topic.posts.last()
    if content:
        if tail.author == user:
            tail.content += '\n\n' + content
            tail.created_at = timezone.now()
            tail.save()
        else:
            tail = topic.posts.create(author=user, content=content)

    Record.new(user=user, topic=topic, post=tail)
    return {tail} | set(topic.posts.filter(created_at__gt=timestamp))

def posts_ajax(request, topic_id):
    timestamp = request.POST.get('timestamp', '1999-01-01 23:59Z')
    topic = get_object_or_404(Topic, id=topic_id)
    modified = get_posts(topic, request.user, timestamp, request.POST.get('content'))
    render = lambda post: render_to_string('posts/post.html', {'post': post})
    html_slugs = [{"id": post.id, "html": render(post)} for post in modified]
    return JsonResponse(html_slugs, safe=False)
