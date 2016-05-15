from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='avatars', default='avatars/default.jpg')
