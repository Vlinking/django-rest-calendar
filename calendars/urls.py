# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from rest_framework import routers

from . import views

# Django REST framework views
router = routers.DefaultRouter()
router.register(r'api/admin/calendars', views.CalendarAdminViewSet)
router.register(r'api/admin/events', views.EventAdminViewSet)
router.register(r'api/user/calendars', views.CalendarOwnedViewSet)
router.register(r'api/user/events', views.EventOwnedViewSet)
router.register(r'api/user/calendar_sharing', views.CalendarSharingViewSet)
router.register(r'api/user/host/invitations', views.InvitationHostViewSet)
router.register(r'api/user/invitee/invitations', views.InvitationInviteeViewSet)

urlpatterns = [
    # API
    url(r'^api/get_calendar_monthly/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)$',
        views.CalendarMonthlyView.as_view()),
    url(r'^api/get_calendar_monthly_detailed/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)$',
        views.CalendarMonthlyDetailedView.as_view()),
    url(r'^api/get_calendar_daily_detailed/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)$',
        views.CalendarDailyDetailedView.as_view()),
    url(r'^api/get_calendar_weekly_detailed/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)$',
        views.CalendarWeeklyDetailedView.as_view()),
    # regular views
    url(r'^$', views.IndexView.as_view(), name='index'),
    # Django REST API
    url(r'^', include(router.urls)),
]