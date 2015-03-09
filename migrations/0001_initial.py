# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fullname', models.CharField(max_length=255, blank=True)),
                ('url', models.URLField(blank=True)),
                ('avatar', models.ImageField(height_field=b'avatar_height', width_field=b'avatar_width', upload_to=b'uploads/dpthoughtdex/authors/')),
                ('avatar_width', models.IntegerField(null=True, blank=True)),
                ('avatar_height', models.IntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
                ('link_name', models.CharField(max_length=255, blank=True)),
                ('message', models.TextField(blank=True)),
                ('visible', models.BooleanField(default=True)),
                ('excerpt', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, blank=True)),
                ('url', models.URLField(blank=True)),
                ('icon', models.ImageField(height_field=b'height', width_field=b'width', upload_to=b'uploads/dpthoughtdex/links/')),
                ('icon_height', models.IntegerField(null=True, blank=True)),
                ('icon_width', models.IntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='link',
            name='source',
            field=models.ForeignKey(to='dpthoughtdex.Source'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='link',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
    ]
