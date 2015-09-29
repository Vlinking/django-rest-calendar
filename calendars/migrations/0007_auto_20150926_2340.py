# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.utils


class Migration(migrations.Migration):

    dependencies = [
        ('calendars', '0006_auto_20150926_2050'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='end',
        ),
        migrations.RemoveField(
            model_name='event',
            name='start',
        ),
        migrations.AddField(
            model_name='event',
            name='_end',
            field=models.DateTimeField(),
        ),
        migrations.AddField(
            model_name='event',
            name='_start',
            field=models.DateTimeField(),
        ),
    ]
