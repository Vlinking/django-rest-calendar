# -*- coding: utf-8 -*-
from rest_framework import serializers

from calendars.models import Calendar, Event


class CalendarSerializer(serializers.HyperlinkedModelSerializer):
    """
    Calendar serializer for admins, allows settings of owners
    """
    class Meta:
        model = Calendar
        fields = ('owner', 'name', 'color')


class CalendarOwnedSerializer(serializers.HyperlinkedModelSerializer):
    """
    Standard Calendar serializer for users, owner is assigned automatically, id field for Ajax actions
    """
    id = serializers.ReadOnlyField()

    class Meta:
        model = Calendar
        fields = ('id', 'name', 'color')


class EventSerializer(serializers.HyperlinkedModelSerializer):
    """
    Event serializer for admins
    """
    id = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = ('id', 'calendar', 'title', 'description', 'timezone', 'type', 'start', 'end')


class EventOwnedSerializer(serializers.HyperlinkedModelSerializer):
    """
    Standard Event serializer for users, id field for Ajax actions
    """
    id = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = ('id', 'calendar', 'title', 'description', 'timezone', 'type', 'start', 'end')
