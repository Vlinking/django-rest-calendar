# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.contrib.auth.models import User

from core.utils import get_timezones


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
    timezone = models.CharField(max_length=50, choices=get_timezones())
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default=NORMAL)
    # same field for both Event types, data will be truncated on 'ALL_DAY' events on model save
    start = models.DateTimeField(default=datetime.datetime.now)
    end = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return self.title

