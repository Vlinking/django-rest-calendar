# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from calendar import Calendar
from datetime import datetime
from django.template import RequestContext
from django.views.generic import TemplateView

from rest_framework import viewsets, permissions, filters

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


class CalendarMonthlyDetailedView(CalendarMonthlyView):
    template_name = 'calendars/large_calendar.html'


class CalendarDailyDetailedView(AjaxRequiredMixin, TemplateView):
    """
    The view of a day, sliced into hours
    """
    template_name = 'calendars/large_day.html'

    def get(self, request, *args, **kwargs):
        data = {
            'hours': [x for x in range(0, 24)]
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
            context.update(
                {
                    'current_month': now.month,
                    'current_year': now.year,
                    'today': now.day,
                    'username': self.request.user.username
                }
            )
        return context




