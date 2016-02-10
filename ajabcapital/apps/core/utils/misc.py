from django.utils import timezone

import calendar
import json
import random
import string
import time

import logging

MONTHS = [
    calendar.month_name[x] for x in range(1,13)
]

def get_reference_no(limit=10):
    possible_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    chosen_chars = ""
    z = 0

    while z <= limit:
        chosen_chars = chosen_chars + random.choice(possible_chars)

        if chosen_chars == '0': #Shouldn't start with a zero
            return get_reference_no(limit=limit)
            
        z += 1

    return chosen_chars

def record_log(request=None, logger=None, message='', level=logging.DEBUG, **kwargs):
    if not logger:
        logger = logging.getLogger(__name__)

    user = request.user
    log_data = {}

    if request is not None:
        log_data['ip_address'] = request.META.get('REMOTE_ADDR')
        log_data['referrer'] = request.META.get('HTTP_REFERER')
        log_data['user_agent'] = request.META.get('HTTP_USER_AGENT')
        log_data['content_type'] = request.META.get('CONTENT_TYPE')

        log_data['method'] = request.method
        log_data['request'] = dict(request.REQUEST.iteritems())
        log_data['url'] = request.get_full_path()

        if user.is_authenticated():
            log_data['user'] = user.email
            log_data['user_role_type'] = user.role_type

    log_data.update(dict(
        message=message,
        timestamp=timezone.now().strftime('%Y-%m-%dT%H:%M:%S%Z'),
        **kwargs
    ))

    logger.log(level, json.dumps(log_data))
