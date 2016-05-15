from django.db import models
from django.contrib.auth import User


class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    avatar = models.ImageField(upload_to='uploads/avatar')
