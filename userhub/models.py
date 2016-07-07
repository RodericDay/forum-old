import os
from datetime import timedelta
from PIL import Image as PImage, ExifTags

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone as tz

from forum.settings import STATIC_ROOT


class Image(models.Model):
    raw = models.ImageField(upload_to='images')
    uploader = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def thumbnail(self):
        infile = self.raw.path
        outfile = infile.replace('images', 'thumbnails', 1)
        if not os.path.isfile(outfile):
            make_thumbnail(infile, outfile)
        return str(self.raw).replace('images', 'thumbnails', 1)

    def full_delete(self):
        if os.path.isfile(self.raw.path):
            os.remove(self.raw.path)
        super().delete()


def make_thumbnail(infile, outfile):
    try:
        im = PImage.open(infile)
    except:
        default = os.path.join(STATIC_ROOT, 'document.png')
        im = PImage.open(default)

    try:
        code = im._getexif()[274]
        mapping = {
            1: lambda im: im,
            3: lambda im: im.transpose(PImage.ROTATE_180),
            6: lambda im: im.transpose(PImage.ROTATE_270),
            8: lambda im: im.transpose(PImage.ROTATE_90),
        }
        im = mapping[code](im)
    except:
        pass

    r = min(300/max(im.width, im.height), 1)
    s = (int(r*im.width), int(r*im.height))
    im.thumbnail(s, PImage.ANTIALIAS)
    im.save(outfile, "JPEG")


class Profile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ForeignKey(Image, default=1)
    timezone = models.CharField(max_length=255, default="Canada/Eastern")
    last_active = models.DateTimeField(default=tz.now)

    @property
    def is_online(self):
        return (tz.now() - self.last_active) < timedelta(minutes=1)


User.get_profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])
