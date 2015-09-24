from django.conf.urls import url, include

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'api/admin/calendars', views.CalendarAdminViewSet)
router.register(r'api/admin/events', views.EventAdminViewSet)
router.register(r'api/user/calendars', views.CalendarOwnedViewSet)

urlpatterns = [
    # API
    url(r'^api/get_calendar_monthly/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)$',
        views.CalendarMonthlyView.as_view()),
    url(r'^api/get_calendar_monthly_detailed/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)$',
        views.CalendarMonthlyDetailedView.as_view()),
    url(r'^api/get_calendar_daily_detailed/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)$',
        views.CalendarDailyDetailedView.as_view()),
    # regular views
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^', include(router.urls)),
]