# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-11 23:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20161212_0254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='posts',
            field=models.ManyToManyField(default=[], to='blog.Post'),
        ),
    ]