# -*- coding: utf-8 -*-
from pytz import all_timezones

# Assume the calendar is for Europeans only (as it currently has only Polish language).
TIMEZONE_CONTINENT = "Europe"


def get_timezones():
    """
    Return timezones. Only one continent will suffice for the scope of the exercise.
    """
    return tuple([(x, x) for x in all_timezones if TIMEZONE_CONTINENT in x])

