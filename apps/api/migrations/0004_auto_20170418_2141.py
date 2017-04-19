# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-19 04:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_taskcollection_identifier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='members',
            field=models.ManyToManyField(blank=True, to='api.Actor'),
        ),
        migrations.AlterField(
            model_name='taskcollection',
            name='tasks',
            field=models.ManyToManyField(blank=True, to='api.Task'),
        ),
    ]
