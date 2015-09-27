# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

from rest_framework import serializers

from core.utils import get_timezones, DEFAULT_TIMEZONE


class CalendarUser(models.Model):
    user = models.OneToOneField(User)
    timezone = models.CharField(max_length=50, choices=get_timezones(), default=DEFAULT_TIMEZONE)


class CalendarUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CalendarUser
        fields = ('user', 'timezone')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')