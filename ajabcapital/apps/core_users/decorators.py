from functools import wraps

from django.utils.decorators import available_attrs
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponseForbidden

from django.contrib.auth.decorators import user_passes_test

import logging

from ..core.utils import record_log
from .models import LogTrail

def user_has_capability(func, capability_codes=[]):
    actual_decorator = user_passes_test(
        lambda u: (u.is_authenticated() and u.is_staff)
    )
    return actual_decorator(func)

def log_access(func):
    @wraps(func, assigned=available_attrs(func))
    def inner(request, *args, **kwargs):
        logger = logging.getLogger(__name__)
        record_log(
            request=request,
            logger=logger,
            category="access",
            action="access_to: %s.%s" % (func.__module__, func.__name__),
            view_args=args,
            view_kwargs=kwargs,
            level=logging.INFO,
            text="log access logged"
        )

        return func(request, *args, **kwargs)
    return inner

def logtrail(func, action_path):
    @wraps(func, assigned=available_attrs(func))
    def inner(user, *args, **kwargs):
        if user.is_authenticated():
            logtrail = LogTrail.objects.create(
                user=request.user,
                action=path
            )
        return func(request, *args, **kwargs)
    return inner
