# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('dpthoughtdex', '0003_auto_20150309_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 9, 10, 36, 15, 207909)),
            preserve_default=True,
        ),
    ]
