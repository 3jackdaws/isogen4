# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-28 16:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_task_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscordWebhook',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('avatar', models.URLField()),
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('token', models.CharField(max_length=68)),
            ],
        ),
        migrations.AlterField(
            model_name='task',
            name='type',
            field=models.IntegerField(choices=[(0, 'Rotating'), (1, 'Periodic')]),
        ),
    ]
