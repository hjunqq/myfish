# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-09 15:43
from __future__ import unicode_literals

import Daily.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('django_comments', '0002_update_user_email_field_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('sentence', models.CharField(blank=True, max_length=500)),
                ('author', models.CharField(blank=True, max_length=100)),
                ('img', models.ImageField(upload_to=Daily.models.get_image_path)),
                ('comments', models.ManyToManyField(blank=True, related_name='comment_by', to='django_comments.Comment')),
                ('likedby', models.ManyToManyField(blank=True, related_name='liked_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'DailyContent',
            },
        ),
    ]
