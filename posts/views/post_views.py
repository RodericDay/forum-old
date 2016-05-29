import json

from django.core.urlresolvers import reverse_lazy
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from posts.models import Post, Topic, Tag, Record


def posts_list(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if not topic.allows_access(request.user):
        return HttpResponseForbidden()

    posts = topic.posts.all()
    Record.new(post=posts.last(), user=request.user, topic=topic)
    context = {"topic": topic, "post_list": posts}
    # fallback in case quickpost attempted with js disabled
    if request.method == "POST":
        content = request.POST['content']
        if content != '':
            post = topic.posts.create(author=request.user, content=content)
            url = topic.get_absolute_url() + "#" + str(post.id)
            return HttpResponseRedirect(url)
        else:
            context['error'] = "empty posts not allowed"
    return render(request, 'posts/post_list.html', context)

def posts_new(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if not topic.allows_access(request.user):
        return HttpResponseForbidden()

    context = {'action': 'new'}
    if request.method == "POST":
        content = request.POST['content']
        if content != '':
            post = topic.posts.create(author=request.user, content=content)
            url = topic.get_absolute_url() + "#" + str(post.id)
            return HttpResponseRedirect(url)
        else:
            context['error'] = "empty posts not allowed"
    return render(request, 'posts/post_form.html', context)

def posts_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if not post.allows_access(request.user):
        return HttpResponseForbidden()

    if request.method == "POST":
        url = post.get_absolute_url()
        if "delete" in request.POST:
            post.content = "[deleted]"
            post.save()
            return HttpResponseRedirect(url)

        content = request.POST['content']
        if content:
            post.content = request.POST['content']
            post.save()
            return HttpResponseRedirect(url)
        else:
            context['error'] = "empty posts not allowed"

    context = {'action': 'edit', 'post': post}
    return render(request, 'posts/post_form.html', context)

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
    return HttpResponseRedirect(url)

def posts_ajax(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if not topic.allows_access(request.user):
        return HttpResponseForbidden()

    if request.method == "POST" and "content" in request.POST:
        content = request.POST['content']
        if content != '':
            topic.posts.create(author=request.user, content=content)
    last = request.POST.get('timestamp', 0)
    modified = topic.posts.filter(modified_at__gt=last)
    Record.new(user=request.user, topic=topic, post=modified.last())
    render = lambda post: render_to_string('posts/post.html', {'post': post})
    html_slugs = [{"id": post.id, "html": render(post)} for post in modified]
    string = json.dumps(html_slugs)
    return HttpResponse(string)
