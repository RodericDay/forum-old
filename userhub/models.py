from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='avatars', default='avatars/default.jpg')
    timezone = models.CharField(max_length=255, default="Canada/Eastern")


User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])
