import os

from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='avatars', default='avatars/default.jpg')
    timezone = models.CharField(max_length=255, default="Canada/Eastern")


User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])


class Image(models.Model):
    raw = models.ImageField(upload_to='images')
    uploader = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)

    def full_delete(self):
        if os.path.isfile(self.raw.path):
            os.remove(self.raw.path)
        super().delete()
