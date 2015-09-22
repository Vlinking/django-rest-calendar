# -*- coding: utf-8 -*-
from django.shortcuts import render

from calendar import Calendar
from datetime import datetime
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


def get_calendar_monthly(request, year, month, day):
    """
    API view for getting the monthly calendar days
    :param request:
    :param year:
    :param month:
    :param day:
    :return:
    """
    if request.is_ajax:
        year, month, day = int(year), int(month), int(day)
        cal = Calendar()
        monthly_days = cal.monthdays2calendar(year, month)
        context = {
            'monthly_days': monthly_days,
            'year': year,
            'month': MONTHS[month],
            'today': day
        }
    return render(request, 'calendars/little_calendar.html', context)


def get_calendar_weekly(request, year, month, day):
    """
    API view for getting weekly calendar days
    :param request:
    :param year:
    :param month:
    :param day:
    :return:
    """
    if request.is_ajax:
        pass


def get_calendar_daily(request, year, month, day):
    """
    API view for getting daily calendar days
    :param request:
    :param year:
    :param month:
    :param day:
    :return:
    """
    if request.is_ajax:
        pass



class IndexView(TemplateView):
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




