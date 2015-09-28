# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.db.models import Q
from calendar import Calendar
from datetime import datetime
from django.template import RequestContext
from django.views.generic import TemplateView

from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from accounts.models import CalendarUser
from calendars.permissions import IsOwnerOrReadOnly
from core.utils import normalize_to_utc

from filters import IsOwnerFilterBackend, IsEventCalendarOwnerFilterBackend
from serializers import CalendarSerializer, EventSerializer, CalendarOwnedSerializer, EventOwnedSerializer, \
    CalendarSharingSerializer, InvitationHostSerializer, InvitationInviteeSerializer
from calendars import models


MONTHS = [
    '',
    'Styczeń',
    'Luty',
    'Marzec',
    'Kwiecień',
    'Maj',
    'Czerwiec',
    'Lipiec',
    'Sierpień',
    'Wrzesień',
    'Październik',
    'Listopad',
    'Grudzień'
]

WEEKDAYS = [
    'Poniedziałek',
    'Wtorek',
    'Środa',
    'Czwartek',
    'Piątek',
    'Sobota',
    'Niedziela'
]


def get_month_wireframe(year, month, day):
    """
    Utility function for getting the layout of month days
    """
    year, month, day = int(year), int(month), int(day)
    cal = Calendar()
    monthly_days = cal.monthdays2calendar(year, month)
    return {
        'monthly_days': monthly_days,
        'year': year,
        'month': MONTHS[month],
        'today': day,
    }


def get_week_wireframe(year, month, day):
    """
    Utility function for returning the current week
    """
    year, month, day = int(year), int(month), int(day)
    cal = Calendar()
    monthly_days = cal.monthdays2calendar(year, month)
    current_week = None
    for week in monthly_days:
        if [i for i, v in enumerate(week) if v[0] == day]:
            current_week = week
    return {
        'week': current_week,
        'year': year,
        'month': MONTHS[month],
        'today': day,
    }


class OwnerMixin(object):
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (IsOwnerFilterBackend,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AjaxRequiredMixin(object):
    """
    A mixin that blocks the view when not using ajax
    """
    def dispatch(self, request, *args, **kwargs):
        if request.is_ajax():
            return super(AjaxRequiredMixin, self).dispatch(request, *args, **kwargs)
        else:
            return render_to_response('calendars/error_no_ajax.html', {},
                context_instance=RequestContext(request))


class DisplayEventsMixin(object):
    """
    A mixin that enables backend support for calendar-based Event filtering
    """
    def filter_calendars(self, request, events):
        calendars_str = request.GET.getlist('calendars[]')
        calendars = [int(x) for x in calendars_str]
        if calendars:
            events = events.filter(calendar__in=calendars,)
        return events


class DailyMixin(object):
    def get_daily_hours(self, request, year, month, day):
        timezone = request.session['django_timezone']
        # filter all-day events
        all_day_events = models.Event.objects.filter(
                Q(calendar__owner=request.user) | Q(calendar__calendarsharing__recipient=request.user),
                type=models.EventMixin.ALL_DAY,
                start__lte=normalize_to_utc(datetime(year, month, day, 23, 59), timezone),
                end__gte=normalize_to_utc(datetime(year, month, day, 0, 0), timezone),
        )
        # filter normal events
        hours = []
        for hour in range(0, 24):
            events = models.Event.objects.filter(
                    Q(calendar__owner=request.user) | Q(calendar__calendarsharing__recipient=request.user),
                    type=models.EventMixin.NORMAL,
                    start__lte=normalize_to_utc(datetime(year, month, day, hour, 59), timezone),
                    end__gte=normalize_to_utc(datetime(year, month, day, hour, 0), timezone),
            )
            events = self.filter_calendars(request, events)
            hours.append((hour, events))
        return (hours, all_day_events)


class CalendarAdminViewSet(viewsets.ModelViewSet):
    """
    Convenience API view for viewing all data for the admin
    and all operations
    """
    queryset = models.Calendar.objects.all()
    serializer_class = CalendarSerializer
    permission_classes = (permissions.IsAdminUser,)


class EventAdminViewSet(viewsets.ModelViewSet):
    """
    Convenience API view for viewing all data for the admin
    and all operations
    """
    queryset = models.Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (permissions.IsAdminUser,)


class CalendarOwnedViewSet(OwnerMixin, CalendarAdminViewSet):
    """
    API view for displaying only calendars that are the current user's
    """
    serializer_class = CalendarOwnedSerializer


class EventOwnedViewSet(EventAdminViewSet):
    """
    API view for displaying only events that are the current user's
    """
    serializer_class = EventOwnedSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    filter_backends = (IsEventCalendarOwnerFilterBackend,)


class CalendarSharingViewSet(OwnerMixin, viewsets.ModelViewSet):
    """
    API view for calendar sharing
    """
    serializer_class = CalendarSharingSerializer
    queryset = models.CalendarSharing.objects.all()


class InvitationHostViewSet(OwnerMixin, viewsets.ModelViewSet):
    """
    API view for creating invitations
    """
    serializer_class = InvitationHostSerializer
    queryset = models.Invitation.objects.all()


class InvitationInviteeViewSet(viewsets.ModelViewSet):
    """
    API view for editing invitations
    """
    serializer_class = InvitationInviteeSerializer
    queryset = models.Invitation.objects.all()


class CalendarMonthlyView(AjaxRequiredMixin, TemplateView):
    """
    The little calendar ajax view
    """
    template_name = 'calendars/little_calendar.html'

    def get(self, request, *args, **kwargs):
        data = get_month_wireframe(*args, **kwargs)
        return render_to_response(self.template_name, data,
            context_instance=RequestContext(request))


class CalendarMonthlyDetailedView(DisplayEventsMixin, CalendarMonthlyView):
    """
    The monthly calendar view including Events
    """
    template_name = 'calendars/large_calendar.html'

    def get(self, request, *args, **kwargs):
        data = get_month_wireframe(*args, **kwargs)
        days_with_events = []
        year = int(kwargs['year'])
        month = int(kwargs['month'])
        timezone = request.session['django_timezone']

        for week in data['monthly_days']:
            week_days = []
            for day in week:
                if day[0] != 0:
                    events = models.Event.objects.filter(
                            Q(calendar__owner=request.user) | Q(calendar__calendarsharing__recipient=request.user),
                            start__lte=normalize_to_utc(datetime(year, month, day[0], 23, 59), timezone),
                            end__gte=normalize_to_utc(datetime(year, month, day[0], 0, 0), timezone),
                    )
                    events = self.filter_calendars(request, events)
                else:
                    events = []
                week_days.append((day[0], day[1], events))
            days_with_events.append(week_days)

        data['monthly_days'] = days_with_events
        return render_to_response(self.template_name, data,
            context_instance=RequestContext(request))


class CalendarWeeklyDetailedView(DisplayEventsMixin, DailyMixin, AjaxRequiredMixin, TemplateView):
    template_name = 'calendars/large_week.html'

    def get(self, request, *args, **kwargs):
        year = int(kwargs['year'])
        month = int(kwargs['month'])
        day = int(kwargs['day'])

        week = get_week_wireframe(*args, **kwargs)['week']
        weekly_days = []
        for day_of_the_week in week:
            if day_of_the_week[0] != 0:
                hours, all_day_events = self.get_daily_hours(request, year, month, day_of_the_week[0])
            else:
                hours, all_day_events = ([], [])
            weekly_days.append((day_of_the_week[0], day_of_the_week[1], hours, all_day_events))

        data = {
            'year': year,
            'month': month,
            'day': day,
            'weekly_days': weekly_days
        }

        return render_to_response(self.template_name, data,
            context_instance=RequestContext(request))


class CalendarDailyDetailedView(DisplayEventsMixin, DailyMixin, AjaxRequiredMixin, TemplateView):
    """
    The view of a day, sliced into hours, including Events
    """
    template_name = 'calendars/large_day.html'

    def get(self, request, *args, **kwargs):
        year = int(kwargs['year'])
        month = int(kwargs['month'])
        day = int(kwargs['day'])

        hours, all_day_events = self.get_daily_hours(request, year, month, day)
        data = {
            'hours': hours,
            'year': year,
            'month': month,
            'day': day,
            'all_day_events': all_day_events
        }
        return render_to_response(self.template_name, data,
            context_instance=RequestContext(request))


class IndexView(TemplateView):
    """
    Index view for the main calendars app page
    """
    template_name = 'calendars/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            try:
                user_settings = CalendarUser.objects.get(user=self.request.user)
            except CalendarUser.DoesNotExist:
                user_settings = None
            else:
                self.request.session['django_timezone'] = user_settings.timezone
            now = datetime.now()
            context.update(
                {
                    'current_month': now.month,
                    'current_year': now.year,
                    'today': now.day,
                    'username': self.request.user.username,
                    'user_settings': user_settings
                }
            )
        return context




