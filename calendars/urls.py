__author__ = 'Bartek'

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^api/get_calendar_monthly/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)$', views.get_calendar_monthly),
    url(r'^$', views.IndexView.as_view(), name='index'),
]