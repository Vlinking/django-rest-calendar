# -*- coding: utf-8 -*-
from django.db.models import Q
from rest_framework import filters

class IsOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Filter for getting only owned objects
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner=request.user)


class IsInviteeFilterBackend(filters.BaseFilterBackend):
    """
    Filter for getting only Invitations we were invited to
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(invitee=request.user)


class IsEventCalendarOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Filter for getting only owned objects, for Events
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(Q(calendar__owner=request.user) | Q(calendar__calendarsharing__recipient=request.user),)


