from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models


class Post(models.Model):
    parent = models.ForeignKey('Post', null=True)
    author = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    content = models.TextField()


class Tag(models.Model):
    ACCESS_CHOICES = [
        (0, "all"),
        (1, "whitelist"),
        (2, "blacklist"),
    ]
    name = models.CharField(max_length=60)
    access_list = models.ManyToManyField(User)
    access_mode = models.IntegerField(default=0, choices=ACCESS_CHOICES)


class Topic(models.Model):
    name = models.CharField(max_length=180)
    author = models.ForeignKey(User)
    posts = models.ManyToManyField(Post)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('posts-list', args=[self.id])
