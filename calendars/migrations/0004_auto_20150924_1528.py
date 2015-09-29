# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('calendars', '0003_auto_20150924_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='end',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='event',
            name='start',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
