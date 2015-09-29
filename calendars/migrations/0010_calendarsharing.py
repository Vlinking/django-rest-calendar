# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('calendars', '0009_auto_20150927_0034'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalendarSharing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'R', max_length=1, choices=[(b'R', b'do odczytu'), (b'W', b'do zapisu')])),
                ('calendar', models.ForeignKey(to='calendars.Calendar')),
                ('owner', models.ForeignKey(related_name='sharing_owner', to=settings.AUTH_USER_MODEL)),
                ('recipient', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
