# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('calendars', '0010_calendarsharing'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('type', models.CharField(default=b'NM', max_length=2, null=True, blank=True, choices=[(b'NM', b'zwyk\xc5\x82y'), (b'AD', b'ca\xc5\x82odzienny')])),
                ('rvsp', models.CharField(default=b'u', max_length=1, null=True, blank=True, choices=[(b'u', b'nie wiem'), (b'm', b'mo\xc5\xbce'), (b'y', b'tak'), (b'n', b'nie')])),
                ('start', models.DateTimeField(default=django.utils.timezone.now)),
                ('end', models.DateTimeField(default=django.utils.timezone.now)),
                ('event', models.ForeignKey(related_name='invited_to', to='calendars.Event')),
                ('invitee', models.ForeignKey(related_name='invitee', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
