import os
from PIL import Image as PImage

from django.contrib.auth.models import User
from django.db import models

from forum.settings import STATIC_ROOT


class Profile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='avatars', default='avatars/default.jpg')
    timezone = models.CharField(max_length=255, default="Canada/Eastern")

    def last_post(self):
        return self.user.post_set.last()


User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])


class Image(models.Model):
    raw = models.ImageField(upload_to='images')
    uploader = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def thumbnail(self):
        o_path = self.raw.path
        t_path = o_path.replace('images', 'thumbnails', 1)
        if not os.path.isfile(t_path):
            try:
                original = PImage.open(o_path)
            except:
                default = os.path.join(STATIC_ROOT, 'document.png')
                original = PImage.open(default)
            r = min(300/max(original.width, original.height), 1)
            s = (int(r*original.width), int(r*original.height))
            thumbnail = original.resize(s)
            thumbnail.save(t_path)
        return str(self.raw).replace('images', 'thumbnails', 1)

    def full_delete(self):
        if os.path.isfile(self.raw.path):
            os.remove(self.raw.path)
        super().delete()
