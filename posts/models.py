from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    parent = models.ForeignKey('Post', null=True)
    author = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
