# -*- coding: utf-8 -*-
from datetime import datetime
from rest_framework import serializers
import pytz

from calendars.models import Calendar, Event, CalendarSharing, Invitation
from core.utils import DEFAULT_TIMEZONE, normalize_to_utc


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
        """
        Save times as UTC after conversion with the timezone set on the event
        """
        tz = self.validated_data.get('timezone', DEFAULT_TIMEZONE)
        start = self.validated_data.get('start', datetime.now())
        end = self.validated_data.get('end', datetime.now())

        start = normalize_to_utc(start, tz)
        end = normalize_to_utc(end, tz)

        self.validated_data['start'] = start
        self.validated_data['end'] = end

        super(EventOwnedSerializer, self).save(**kwargs)


class CalendarSharingSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for shared calendars
    """
    class Meta:
        model = CalendarSharing
        fields = ('owner', 'recipient', 'calendar', 'type')


class InvitationHostSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for adding invitations
    """
    class Meta:
        model = Invitation
        fields = ('invitee', 'event')


class InvitationInviteeSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for viewing/editing invitations
    """
    class Meta:
        model = Invitation
        fields = ('title', 'description', 'type', 'start', 'end', 'rvsp')




