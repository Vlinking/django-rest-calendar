# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.db.models import Q
from calendar import Calendar
from datetime import datetime
from django.template import RequestContext
from django.views.generic import TemplateView

from rest_framework import viewsets, permissions, filters
from accounts.models import CalendarUser

from filters import IsOwnerFilterBackend, IsEventCalendarOwnerFilterBackend
from serializers import CalendarSerializer, EventSerializer, CalendarOwnedSerializer, EventOwnedSerializer
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
        'today': day
    }


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


class CalendarOwnedViewSet(CalendarAdminViewSet):
    """
    API view for displaying only calendars that are the current user's
    """
    serializer_class = CalendarOwnedSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (IsOwnerFilterBackend,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class EventOwnedViewSet(EventAdminViewSet):
    """
    API view for displaying only events that are the current user's
    """
    serializer_class = EventOwnedSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (IsEventCalendarOwnerFilterBackend,)


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


class CalendarMonthlyView(AjaxRequiredMixin, TemplateView):
    """
    The little calendar ajax view
    """
    template_name = 'calendars/little_calendar.html'

    def get(self, request, *args, **kwargs):
        data = get_month_wireframe(*args, **kwargs)
        return render_to_response(self.template_name, data,
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

        for week in data['monthly_days']:
            week_days = []
            for day in week:
                if day[0] != 0:
                    events = models.Event.objects.filter(
                            calendar__owner=request.user,
                            start__lte=datetime(year, month, day[0], 23, 59),
                            end__gte=datetime(year, month, day[0], 0, 0),
                    )
                    events = self.filter_calendars(request, events)
                else:
                    events = []
                week_days.append((day[0], day[1], events))
            days_with_events.append(week_days)

        data['monthly_days'] = days_with_events
        return render_to_response(self.template_name, data,
            context_instance=RequestContext(request))


class CalendarDailyDetailedView(DisplayEventsMixin, AjaxRequiredMixin, TemplateView):
    """
    The view of a day, sliced into hours, including Events
    """
    template_name = 'calendars/large_day.html'

    def get(self, request, *args, **kwargs):
        year = int(kwargs['year'])
        month = int(kwargs['month'])
        day = int(kwargs['day'])
        # filter all-day events
        all_day_events = models.Event.objects.filter(
                calendar__owner=request.user,
                type=models.Event.ALL_DAY,
                start__lte=datetime(year, month, day, 23, 59),
                end__gte=datetime(year, month, day, 0, 0),
        )
        # filter normal events
        hours = []
        for hour in range(0, 24):
            events = models.Event.objects.filter(
                    calendar__owner=request.user,
                    type=models.Event.NORMAL,
                    start__lte=datetime(year, month, day, hour, 59),
                    end__gte=datetime(year, month, day, hour, 0),
            )
            events = self.filter_calendars(request, events)
            hours.append((hour, events))

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
            now = datetime.now()
            user_settings = CalendarUser.objects.get(user=self.request.user)
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




