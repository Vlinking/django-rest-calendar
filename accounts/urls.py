# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from rest_framework import routers

import views

router = routers.DefaultRouter()
router.register(r'api/admin/calendar_users', views.CalendarUserAdminViewSet)
router.register(r'api/admin/users', views.UserAdminViewSet)

urlpatterns = [
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^profile/$', views.ProfileView.as_view()),
    url(r'^', include(router.urls)),
]