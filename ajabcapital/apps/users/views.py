from django.contrib.auth import (login as auth_login, authenticate)
from django.contrib.auth.decorators import login_required

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse, resolve

from django.db.models import Sum, Avg, Max, Q, Count
from django.db import transaction as db_transaction

from django.shortcuts import render, get_object_or_404, redirect
from django.template.response import TemplateResponse

from django.http import (
    Http404, JsonResponse, HttpResponseForbidden, 
    HttpResponse, HttpResponseRedirect
)

from django.utils import timezone
from django.utils.text import slugify

from django.views.decorators.http import require_POST, require_GET

import simplejson as json
import random
import datetime

from decimal import Decimal as D

from ..core import (
    utils as core_utils
)
from . import (
    api as auth_api,
    forms as auth_forms,
    utils as auth_utils, 
    models as user_models
)

import logging

def dashboard(request):
    logger = logging.getLogger(__name__)

    if not auth_utils.is_capable(request.user, 'users.dashboard'):
        return HttpResponseForbidden('Access Denied')

#-------------------- activate/deactivate
@login_required
@require_POST
def activate_user(request):
    logger = logging.getLogger(__name__)

    if not auth_utils.is_capable(request.user, 'users.activate'):
        return HttpResponseForbidden('Access Denied')

    user_id = core_utils.get_int_or_None(request.objects.get('user_id'))

    #get the user to activate
    user = get_object_or_404(user_models.User, id=user_id)

    with db_transaction.atomic():
        logger.debug("start: action='users.activate' request_user_id=%s user_id=%s" % (request.user, user_id))
        auth_api.activate_user(user)
        logger.debug("end: action='users.activate' request_user_id=%s user_id=%s" % (request.user, user_id))

        core_utils.leave_user_message(
            request, "INFO", "You have successfully activated user %s" % user.get_full_name()
        )

    #where to redirect to after save
    redirect_to = request.POST.get('redirect_to', 'users:dashboard')
    return redirect(redirect_to)

@login_required
@require_POST
def deactivate_user(request):
    logger = logging.getLogger(__name__)

    if not auth_utils.is_capable(request.user, 'users.deactivate'):
        return HttpResponseForbidden('Access Denied')

    #get the user to activate
    user_id = core_utils.get_int_or_None(request.objects.get('user_id'))
    user = get_object_or_404(user_models.User, id=user_id)

    with db_transaction.atomic():
        logger.debug("start: action='users.activate' request_user_id=%s user_id=%s" % (request.user, user_id))
        auth_api.deactivate_user()
        logger.debug("end: action='users.activate' request_user_id=%s user_id=%s" % (request.user, user_id))

        core_utils.leave_user_message(
            request, "INFO", "You have successfully deactivated user %s" % user.get_full_name()
        )

    #where to redirect to after save
    redirect_to = request.POST.get('redirect_to', 'users:dashboard')
    return redirect(redirect_to)

#--------------------
@login_required
@require_POST
def add_user(request):
    logger = logging.getLogger(__name__)

    form = AddPartnerUserForm(request.POST)

    if form.is_valid():
        data = form.cleaned_data

        with db_transaction.atomic():
            user = auth_api.create_user(data)
            logger.debug(
                "action='users.add.partner' request_user_id=%s user_id=%s" % (
                    request.user, user.id
                )
            )

            redirect_to = request.POST.get('redirect_to', 'users:dashboard')
            return redirect(redirect_to)
