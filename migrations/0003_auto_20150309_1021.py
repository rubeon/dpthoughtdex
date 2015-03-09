# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('dpthoughtdex', '0002_auto_20150309_1012'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='author',
            field=models.ForeignKey(default='', to='dpthoughtdex.Author'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='link',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 9, 10, 20, 40, 110597)),
            preserve_default=True,
        ),
    ]
