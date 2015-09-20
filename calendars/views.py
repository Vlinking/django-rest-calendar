# -*- coding: utf-8 -*-
from django.shortcuts import render

from calendar import Calendar
from datetime import datetime


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


def index(request):
    now = datetime.now()
    cal = Calendar()
    current_month = cal.monthdays2calendar(now.year, now.month)
    context = {
        'current_month': current_month,
        'month': MONTHS[now.month],
        'year': now.year
    }

    return render(request, 'calendars/index.html', context)


class CustomCalendar(Calendar):
    pass




