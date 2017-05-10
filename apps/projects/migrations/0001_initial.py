# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-09 05:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('short_description', models.CharField(max_length=400)),
                ('short_name', models.CharField(max_length=32, unique=True)),
                ('picture', models.ImageField(upload_to='')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(blank=True)),
                ('text', models.TextField()),
                ('external_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Technology',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('short_description', models.CharField(max_length=400)),
                ('external_url', models.URLField()),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='technologies',
            field=models.ManyToManyField(blank=True, to='projects.Technology'),
        ),
    ]