# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-21 18:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_tag_topic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=60, unique=True),
        ),
    ]
