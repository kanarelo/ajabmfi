from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.http import (Http404, JsonResponse, HttpResponseForbidden)
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST, require_GET
from django.utils import timezone

from django.db.models import (Sum, Avg, Max, Q, Count)
from django.db import (transaction as db_transaction)

import json
import random

def dashboard(request):
    context = dict()

    context.update(
        portfolio_at_risk_by_product={},
        portfolio_at_risk_by_balance={},
        provision_for_bad_debt={},
        top_5_accounts_in_arrears={},
        repayment_trends_chart={},
        disbursal_trends_chart={},
        top_5_non_performing_products={}
    )

    return TemplateResponse(request, "risk_management/dashboard.html", context)

def portfolio_at_risk(request):
    context = {}
    return TemplateResponse(request, "risk_management/portfolio_at_risk.html", context)
