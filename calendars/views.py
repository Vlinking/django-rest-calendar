# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response

from calendar import Calendar
from datetime import datetime
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

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


class IndexView(TemplateView):
    """
    Index view for the main calendars app page
    """
    template_name = 'calendars/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        if not self.request.user.is_authenticated():
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




