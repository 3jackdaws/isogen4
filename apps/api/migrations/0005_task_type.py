# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-19 15:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20170418_2141'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='type',
            field=models.IntegerField(choices=[(1, 'Rotating'), (2, 'Periodic')], default=1),
            preserve_default=False,
        ),
    ]
