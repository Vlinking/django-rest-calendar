__author__ = 'Bartek'

from django.conf.urls import url

from . import views


urlpatterns = [
    # API
    url(r'^api/get_calendar_monthly/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)$', views.CalendarMonthlyView.as_view()),
    url(r'^api/get_calendar_monthly_detailed/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)$',
        views.CalendarMonthlyDetailedView.as_view()),
    # regular views
    url(r'^$', views.IndexView.as_view(), name='index'),
]