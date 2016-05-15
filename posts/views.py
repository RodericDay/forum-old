from django.shortcuts import render

from posts.models import Post

def posts_view(request):
    context = {"posts": Post.objects.all()}
    return render(request, 'main.html', context)
