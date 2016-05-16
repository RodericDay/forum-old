from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.template.loader import render_to_string
from posts.models import Post

@login_required(login_url='/login/')
def posts_delete(request, pk):
    post = Post.objects.get(id=pk)
    if not (request.user.is_superuser or request.user == post.author):
        return HttpResponseForbidden()
    if request.method == "POST":
        post.delete()
        return HttpResponseRedirect('/#latest')
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
            url = "/#{}".format(post.id)
            return HttpResponseRedirect(url)
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
    if request.method == "POST":
        content = request.POST['content']
        if content != '':
            Post.objects.create(author=request.user, content=content)
            return HttpResponseRedirect('/')
        else:
            context['error'] = "empty posts not allowed"
    return render(request, 'posts/list.html', context)

@login_required(login_url='/login/')
def posts_status(request):
    f = lambda p: render_to_string('posts/post.html', {'post': p})
    if request.method == "POST" and "content" in request.POST:
        content = request.POST['content']
        if content != '':
            Post.objects.create(author=request.user, content=content)
    html = '<hr>' + '<hr>'.join(f(p) for p in Post.objects.all())
    return HttpResponse(html)
