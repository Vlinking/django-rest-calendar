# -*- coding: utf-8 -*-
import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from mock import mock

from model_mommy import mommy
from accounts.models import CalendarUser

from calendars.models import Event, Calendar, Invitation
from calendars.views import get_month_wireframe, CalendarMonthlyView, IndexView


# unit tests
class ModelsCreationTest(TestCase):
    def common_model_test(self, klass, unicode_prop):
        obj = mommy.make(klass)
        self.assertTrue(isinstance(obj, klass))
        self.assertEqual(obj.__unicode__(), getattr(obj, unicode_prop))

    def test_calendar_creation(self):
        """
        Do we have Calendar model
        """
        self.common_model_test(Calendar, 'name')

    def test_event_creation(self):
        """
        Do we have Event model
        """
        self.common_model_test(Event, 'title')

    def test_invitation_creation(self):
        """
        Do we have Invitation model
        """
        self.common_model_test(Invitation, 'title')


class MonthWireframeTest(TestCase):
    def test_get_month_wireframe(self):
        """
        Unit test for the wireframe monthly function
        """
        year, month, day = 2015, 9, 28
        self.assertEqual(
            get_month_wireframe(year, month, day),
            {'monthly_days': [
                    [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)],
                    [(7, 0), (8, 1), (9, 2), (10, 3), (11, 4), (12, 5), (13, 6)],
                    [(14, 0), (15, 1), (16, 2), (17, 3), (18, 4), (19, 5), (20, 6)],
                    [(21, 0), (22, 1), (23, 2), (24, 3), (25, 4), (26, 5), (27, 6)],
                    [(28, 0), (29, 1), (30, 2), (0, 3), (0, 4), (0, 5), (0, 6)]
                ],
            'year': 2015,
            'month': 'Wrzesień',
            'today': 28,
            }
        )


class CalendarMonthlyViewTest(TestCase):
    def setUp(self):
        self.obj = CalendarMonthlyView()

    @mock.patch('calendars.views.get_month_wireframe')
    def test_get(self, m):
        """
        Test the get function
        """
        m.result = 'whatever'
        request = mock.Mock()
        self.obj.get(request)
        self.assertTrue(m.called)


class IndexViewTest(TestCase):
    def setUp(self):
        self.obj = IndexView()
        self.obj.request = mock.Mock()
        self.obj.request.user = mommy.make('User')
        self.obj.request.session = {}

    def test_get_context_data_authenticated(self):
        """
        Test for the authenticated, non exception route
        """
        calendar_user = mommy.make(CalendarUser, user=self.obj.request.user)
        context = self.obj.get_context_data()
        now = datetime.datetime.now()
        self.assertEqual(context, {
            'current_month': now.month,
            'current_year': now.year,
            'today': now.day,
            'username': self.obj.request.user.username,
            'user_settings': calendar_user,
            'view': self.obj,
        })

    def test_get_context_data_not_authenticated(self):
        """
        Test for the unauthenticated route
        """
        self.obj.request.user.is_authenticated = mock.MagicMock(return_value=False)
        context = self.obj.get_context_data()
        self.assertEqual(context, {'view': self.obj})


    def test_get_context_data_no_object(self):
        """
        Test for the authenticated, exception route
        """
        context = self.obj.get_context_data()
        now = datetime.datetime.now()
        self.assertEqual(context, {
            'current_month': now.month,
            'current_year': now.year,
            'today': now.day,
            'username': self.obj.request.user.username,
            'user_settings': None,
            'view': self.obj,
        })


# class APIViewTests(TestCase):
#     def setUp(self):
#         admin = mommy.make(User, is_staff=True)
#         user = mommy.make(User)
#
#
#     def test_monthly_view_test(self):
#         pass
#
#     def test_weekly_view_test(self):
#         pass
#
#     def test_daily_view_test(self):
#         pass
#
#     def test_calendar_owner_access(self):
#         pass
#
#     def test_calendar_anon_access(self):
#         pass
#
#     def test_calendar_non_ajax_access(self):
#         pass




