import json

from django.core.urlresolvers import reverse_lazy
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from posts.models import Post, Topic, Tag


def posts_list(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if not topic.allows_access(request.user):
        return HttpResponseForbidden()

    context = {"topic": topic, "post_list": topic.posts.all()}
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

    context = {'action': 'edit', 'post': post}
    if request.method == "POST":
        content = request.POST['content']
        if content != '':
            post.content = request.POST['content']
            post.save()
            url = post.get_absolute_url()
            return HttpResponseRedirect(url)
        else:
            context['error'] = "empty posts not allowed"
    return render(request, 'posts/post_form.html', context)

def posts_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if not post.allows_access(request.user):
        return HttpResponseForbidden()

    if request.method == "POST":
        post.content = "[deleted]"
        post.save()
        url = post.get_absolute_url()
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
    render = lambda post: render_to_string('posts/post.html', {'post': post})
    html_slugs = [{"id": post.id, "html": render(post)} for post in modified]
    string = json.dumps(html_slugs)
    return HttpResponse(string)
