from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist


from django.http import (
    Http404, JsonResponse, HttpResponseForbidden
)

from django.shortcuts import resolve_url, render, get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST, require_GET

import json
import random
import logging

from . import (forms, facades)

from ..core import (
    utils as core_utils,
    forms as core_forms
)

def dashboard(request):

    context = dict(
        quick_accounts=facades.get_quick_accounts(user),
        net_portfolio=facades.get_net_portfolio(user),
        overdues_by_product=facades.get_overdues_by_product(user),
        gross_portfolio_by_product=facades.get_gross_portfolio_by_product(user),
        loan_funds_perfomance=facades.get_loan_funds_perfomance(user),
        portfolio_at_risk=facades.get_portfolio_at_risk_by_level(user),
        key_perfomance_indicators=facades.get_key_perfomance_indicators(user)
    )

    return TemplateResponse(request, "accounting/dashboard.html", {})
