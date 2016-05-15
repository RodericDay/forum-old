from django.shortcuts import render
from django.http import HttpResponseRedirect

from posts.models import Post

def posts_new(request):
    context = {}
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
    return render(request, 'main.html', context)
