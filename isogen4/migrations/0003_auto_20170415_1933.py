# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-15 19:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isogen4', '0002_auto_20170415_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='access_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]