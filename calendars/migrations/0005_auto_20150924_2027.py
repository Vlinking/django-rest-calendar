# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calendars', '0004_auto_20150924_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='type',
            field=models.CharField(default=b'NM', max_length=2, choices=[(b'NM', b'zwyk\xc5\x82y'), (b'AD', b'ca\xc5\x82odzienny')]),
        ),
    ]
