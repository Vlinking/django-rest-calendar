# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone as _timezone

from core.utils import get_timezones, DEFAULT_TIMEZONE


class Calendar(models.Model):
    """
    Stores info about calendars
    """
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    # will be stored in RGB
    # or better, a custom field can be done
    color = models.CharField(max_length=6)

    def __unicode__(self):
        return self.name


class Event(models.Model):
    """
    Stores info about events
    """
    NORMAL = 'NM'
    ALL_DAY = 'AD'
    TYPE_CHOICES = (
        (NORMAL, 'zwykły'),
        (ALL_DAY, 'całodzienny'),
    )

    calendar = models.ForeignKey(Calendar)
    title = models.CharField(max_length=50)
    description = models.TextField()
    timezone = models.CharField(max_length=50, choices=get_timezones(), default=DEFAULT_TIMEZONE)
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default=NORMAL)
    # same field for both Event types, data will be truncated on 'ALL_DAY' events on model save
    start = models.DateTimeField(default=_timezone.now)
    end = models.DateTimeField(default=_timezone.now)

    def __unicode__(self):
        return self.title


class CalendarSharing(models.Model):
    """
    Many to many relation containing the calendar sharing
    """
    READ = 'R'
    WRITE = 'W'
    TYPE_CHOICES = (
        (READ, 'do odczytu'),
        (WRITE, 'do zapisu'),
    )

    owner = models.ForeignKey(User, related_name='sharing_owner')
    recipient = models.ForeignKey(User)
    calendar = models.ForeignKey(Calendar)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default=READ)



