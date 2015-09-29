# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calendars', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='calendar',
            field=models.ForeignKey(default=1, to='calendars.Calendar'),
            preserve_default=False,
        ),
    ]
