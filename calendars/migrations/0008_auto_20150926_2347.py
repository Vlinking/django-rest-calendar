# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calendars', '0007_auto_20150926_2340'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='_end',
            new_name='end',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='_start',
            new_name='start',
        ),
    ]
