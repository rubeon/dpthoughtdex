# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('dpthoughtdex', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 9, 10, 12, 23, 342656)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='author',
            name='fullname',
            field=models.CharField(unique=True, max_length=255, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='source',
            name='name',
            field=models.CharField(unique=True, max_length=255, blank=True),
            preserve_default=True,
        ),
    ]
