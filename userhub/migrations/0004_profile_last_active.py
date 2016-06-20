# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-07 13:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('userhub', '0003_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='last_active',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]