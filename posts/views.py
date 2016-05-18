import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.template.loader import render_to_string

from posts.models import Post


def posts_delete(request, pk):
    post = Post.objects.get(id=pk)
    if not (request.user.is_superuser or request.user == post.author):
        return HttpResponseForbidden()
    if request.method == "POST":
        post.delete()
        return HttpResponseRedirect('/#latest')
    return render(request, 'posts/delete.html', {'post': post})

def posts_edit(request, pk):
    post = Post.objects.get(id=pk)
    if request.user != post.author:
        return HttpResponseForbidden()
    context = {'action': 'edit', 'post': post}
    if request.method == "POST":
        content = request.POST['content']
        if content != '':
            post.content = request.POST['content']
            post.save()
            url = "/#{}".format(post.id)
            return HttpResponseRedirect(url)
        else:
            context['error'] = "empty posts not allowed"
    return render(request, 'posts/form.html', context)

def posts_new(request):
    context = {'action': 'new'}
    if request.method == "POST":
        content = request.POST['content']
        if content != '':
            Post.objects.create(author=request.user, content=content)
            return HttpResponseRedirect('/')
        else:
            context['error'] = "empty posts not allowed"
    return render(request, 'posts/form.html', context)

def posts_view(request):
    context = {"posts": Post.objects.all()}
    if request.method == "POST":
        content = request.POST['content']
        if content != '':
            Post.objects.create(author=request.user, content=content)
            return HttpResponseRedirect('/')
        else:
            context['error'] = "empty posts not allowed"
    return render(request, 'posts/list.html', context)

def posts_status(request):
    if request.method == "POST" and "content" in request.POST:
        content = request.POST['content']
        if content != '':
            Post.objects.create(author=request.user, content=content)
    last = request.POST.get('timestamp', 0)
    modified = Post.objects.filter(modified_at__gt=last)
    render = lambda post: render_to_string('posts/post.html', {'post': post})
    html_slugs = [{"id": post.id, "html": render(post)} for post in modified]
    string = json.dumps(html_slugs)
    return HttpResponse(string)
