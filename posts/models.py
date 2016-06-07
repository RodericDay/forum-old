from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models


class Post(models.Model):
    parent = models.ForeignKey('Post', null=True)
    author = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    content = models.TextField()

    def get_absolute_url(self):
        return reverse('posts-edit', args=[self.id])

    def allows_access(self, user):
        return user.is_superuser or user == self.author


class Tag(models.Model):
    ACCESS_CHOICES = [
        (0, "all"),
        (1, "whitelist"),
        (2, "blacklist"),
    ]
    name = models.CharField(max_length=60, unique=True)
    access_list = models.ManyToManyField(User)
    access_mode = models.IntegerField(default=0, choices=ACCESS_CHOICES)

    def get_absolute_url(self):
        return reverse('tags-edit', args=[self.name])


class Topic(models.Model):
    name = models.CharField(max_length=180)
    author = models.ForeignKey(User)
    posts = models.ManyToManyField(Post)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('posts-list', args=[self.id])

    def tags_as_string(self):
        return " ".join(tag.name for tag in self.tags.all())

    def allows_access(self, user):
        for tag in self.tags.all().filter(access_mode=1): # whitelist
            if not user in tag.access_list.all():
                return False
        for tag in self.tags.all().filter(access_mode=2): # blacklist
            if user in tag.access_list.all():
                return False
        return True


class Record(models.Model):
    user = models.ForeignKey(User)
    topic = models.ForeignKey(Topic)
    post = models.ForeignKey(Post, default=0)

    class Meta:
        unique_together = ("user", "topic")

    @classmethod
    def new(cls, user, topic, post):
        record, new = cls.objects.get_or_create(user=user, topic=topic)
        record.post = post
        record.save()
