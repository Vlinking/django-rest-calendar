import pytz

from django.utils import timezone

class TimezoneMiddleware(object):
    """
    Middleware class that allows us to set the current timezone
    """
    def process_request(self, request):
        tzname = request.session.get('django_timezone')
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()