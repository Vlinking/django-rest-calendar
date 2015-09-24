from django.contrib.auth.models import User
from django.db import models
from rest_framework import serializers


class CalendarUser(models.Model):
    user = models.OneToOneField(User)
    timezone = models.CharField(max_length=50)


class CalendarUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CalendarUser
        fields = ('user', 'timezone')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')