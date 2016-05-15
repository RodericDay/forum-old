from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from posts.models import Post

@login_required(login_url='/login/')
def posts_delete(request, pk):
    post = Post.objects.get(id=pk)
    if not (request.user.is_superuser or request.user == post.author):
        return HttpResponseForbidden()
    if request.method == "POST":
        post.delete()
        return HttpResponseRedirect('/')
    return render(request, 'posts/delete.html', {'post': post})

@login_required(login_url='/login/')
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
            return HttpResponseRedirect('/')
        else:
            context['error'] = "empty posts not allowed"
    return render(request, 'posts/form.html', context)

@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
def posts_view(request):
    context = {"posts": Post.objects.all()}
    return render(request, 'main.html', context)
