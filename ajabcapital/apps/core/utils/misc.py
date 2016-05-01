from dateutil.tz import tzutc
from django.utils import timezone

import calendar
import simplejson as json
import random
import string
import time

import logging

MONTHS = [
    calendar.month_name[x] for x in range(1,13)
]


UTC = tzutc()

def serialize_date(dt):
    """
    Serialize a date/time value into an ISO8601 text representation
    adjusted (if needed) to UTC timezone.

    For instance:
    >>> serialize_date(datetime(2012, 4, 10, 22, 38, 20, 604391))
    '2012-04-10T22:38:20.604391Z'
    """
    if hasattr(dt, "tzinfo"):
        if dt.tzinfo:
            dt = dt.astimezone(UTC).replace(tzinfo=None)
        return dt.isoformat() + 'Z'

def get_reference_no(limit=10):
    possible_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    chosen_chars = ""
    z = 0

    while (z <= limit):
        chosen_chars = (chosen_chars + random.choice(possible_chars))
        z += 1

    return chosen_chars

def record_log(request=None, logger=None, message='', user=None, level=logging.DEBUG, *args, **kwargs):
    if not logger:
        logger = logging.getLogger(__name__)

    log_data = {}

    if user is None: 
        if request is not None:
            user = request.user
        else:
            raise Exception("Please provide the user or a request object")

    elif request is not None:
        log_data['ip_address'] = request.META.get('REMOTE_ADDR')
        log_data['referrer'] = request.META.get('HTTP_REFERER')
        log_data['user_agent'] = request.META.get('HTTP_USER_AGENT')
        log_data['content_type'] = request.META.get('CONTENT_TYPE')

        log_data['method'] = request.method
        log_data['request'] = dict(request.REQUEST.iteritems())
        log_data['url'] = request.get_full_path()

    if user.is_authenticated():
        log_data['user'] = user.email

    log_data.update(dict(
        message=message,
        timestamp=timezone.now(),
        **kwargs
    ))

    logger.log(level, json.dumps(log_data, default=serialize_date))
