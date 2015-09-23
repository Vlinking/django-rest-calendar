__author__ = 'Bartek'

from django.conf.urls import url

import views

urlpatterns = [
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^profile/$', views.ProfileView.as_view())
]