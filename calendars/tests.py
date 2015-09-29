# -*- coding: utf-8 -*-
import datetime
from django.contrib.auth.models import User
import json
from django.test import TestCase

from mock import mock
from model_mommy import mommy
from rest_framework.test import APITestCase
from accounts.models import CalendarUser
from calendars.models import Invitation, Event, Calendar
import dateutil.parser as parser

from calendars.views import get_month_wireframe, CalendarMonthlyView, IndexView


# unit tests
from core.utils import DEFAULT_TIMEZONE


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


class IndexViewTest(TestCase):
    def setUp(self):
        self.obj = IndexView()
        self.obj.request = mock.Mock()
        self.obj.request.user = mommy.make('User')
        self.obj.request.session = {}

    def test_get_context_data_authenticated(self):
        """
        Test for the authenticated, no exception route
        """
        calendar_user = mommy.make(CalendarUser, user=self.obj.request.user)
        context = self.obj.get_context_data()
        now = datetime.datetime.now()
        self.assertEqual(context, {
            'current_month': now.month,
            'current_year': now.year,
            'today': now.day,
            'username': self.obj.request.user.username,
            'timezone': DEFAULT_TIMEZONE,
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
            'timezone': u'UTC',
            'view': self.obj,
        })


# functional tests
class UsersMixin(object):
    def setUp(self):
        self.admin = mommy.make(User, is_staff=True)
        self.user = mommy.make(User)


class AdminViewMixin(UsersMixin):
    url = ''
    def test_view_anonymous(self):
        """
        Test anonymous view
        """
        response = self.client.get(self.url)
        self.assertEqual(json.loads(response.content), {
            u'detail': u'Authentication credentials were not provided.',
        })

    def test_view_normal_user(self):
        """
        Test normal user view
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(json.loads(response.content), {
            u'detail': u'You do not have permission to perform this action.',
        })


class CalendarAdminViewSetTest(AdminViewMixin, APITestCase):
    url = '/calendars/api/admin/calendars/'

    def setUp(self):
        super(CalendarAdminViewSetTest, self).setUp()
        self.calendar = mommy.make('Calendar', owner=self.user)

    def test_view_authenticated(self):
        """
        Test admin view
        """
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.url)
        self.assertEqual(json.loads(response.content), [{
            u'owner': u"http://testserver/accounts/api/admin/users/{}/".format(self.user.id),
            u'name': self.calendar.name,
            u'color': self.calendar.color,
        }])


class EventAdminViewSetTest(AdminViewMixin, APITestCase):
    url = '/calendars/api/admin/events/'

    def setUp(self):
        super(EventAdminViewSetTest, self).setUp()
        self.calendar = mommy.make('Calendar', owner=self.user)
        self.event = mommy.make('Event', calendar=self.calendar)

    def test_view_authenticated(self):
        """
        Test admin view
        """
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.url)
        # ISO 8601
        self.assertEqual(json.loads(response.content), [{
            u'calendar': u"http://testserver/calendars/api/user/calendars/{}/"
                         .format(self.calendar.id),
            u'title': self.event.title,
            u'description': self.event.description,
            u'timezone': self.event.timezone,
            u'type': self.event.type,
            u'start': (parser.parse(unicode(self.event.start))).isoformat().replace('000+00:00', '000Z'),
            u'end': (parser.parse(unicode(self.event.end))).isoformat().replace('000+00:00', '000Z'),
            u'id': self.event.id,
        }])



