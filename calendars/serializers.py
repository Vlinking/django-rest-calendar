from rest_framework import serializers

from calendars.models import Calendar, Event


class CalendarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Calendar
        fields = ('owner', 'name', 'color')


class CalendarOwnedSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Calendar
        fields = ('id', 'name', 'color')


class EventSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = ('id', 'calendar', 'title', 'description', 'timezone', 'type', 'start', 'end')


class EventOwnedSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = ('id', 'calendar', 'title', 'description', 'timezone', 'type', 'start', 'end')
