# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-07-07 00:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userhub', '0004_profile_last_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='userhub.Image'),
        ),
    ]
