# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-02 04:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_urlcache'),
    ]

    operations = [
        migrations.AddField(
            model_name='urlcache',
            name='cache_invalid_at',
            field=models.TimeField(auto_now_add=True, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='urlcache',
            name='hash',
            field=models.BigIntegerField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='urlcache',
            name='url',
            field=models.URLField(),
        ),
    ]