# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calendars', '0002_event_calendar'),
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
    ]
