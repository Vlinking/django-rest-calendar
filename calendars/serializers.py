# -*- coding: utf-8 -*-
from datetime import datetime
from rest_framework import serializers

from calendars.models import Calendar, Event, CalendarSharing


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

    def save(self, **kwargs):
        tz = self.context['request'].session['django_timezone']
        # use self.validated_data, it goes on to be saved
        # save times as UTC after conversion with the timezone set on the event
        # start = self.validated_data.get('start', datetime.now())
        # end = self.validated_data.get('end', datetime.now())

        super(EventOwnedSerializer, self).save(**kwargs)


class CalendarSharingSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for shared calendars
    """
    class Meta:
        model = CalendarSharing
        fields = ('owner', 'recipient', 'calendar', 'type')
