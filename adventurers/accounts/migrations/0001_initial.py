# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-12 14:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import easy_thumbnails.fields
import userena.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('missionboard', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mugshot', easy_thumbnails.fields.ThumbnailerImageField(blank=True, help_text='A personal image displayed in your profile.', upload_to=userena.models.upload_to_mugshot, verbose_name='mugshot')),
                ('privacy', models.CharField(choices=[('open', 'Open'), ('registered', 'Registered'), ('closed', 'Closed')], default='registered', help_text='Designates who can view your profile.', max_length=15, verbose_name='privacy')),
                ('level', models.IntegerField(default=0)),
                ('bios', models.TextField()),
                ('contact', models.TextField()),
                ('missions_completed', models.ManyToManyField(blank=True, related_name='missions_completed', to='missionboard.Mission')),
                ('missions_failed', models.ManyToManyField(blank=True, related_name='missions_failed', to='missionboard.Mission')),
                ('missions_wip', models.ManyToManyField(blank=True, related_name='missions_wip', to='missionboard.Mission')),
                ('partners', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('skills', models.ManyToManyField(to='missionboard.Skill')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='my_profile', to=settings.AUTH_USER_MODEL, verbose_name='使用者')),
            ],
            options={
                'abstract': False,
                'permissions': (('view_profile', 'Can view profile'),),
            },
        ),
    ]
