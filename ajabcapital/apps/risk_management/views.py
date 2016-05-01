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
        top_5_non_performing_products={},
        npl_ratio=23,
        return_on_rwa=30,
        capital_adequacy_ratio=34,
        probability_of_default=4.3,
        expected_loss="500M",
        expected_loss_percentage=40,
        risk_weighted_assets=1428992999,
        exposure_at_default="1.4B",
        npl_by_credit_rating=[
            {'name': '200-300', 'value': 223992200, 'color': '#EFF2DD'},
            {'name': '301-400', 'value': 123992200, 'color': '#F6EA8C'},
            {'name': '401-500', 'value': 223992200, 'color': '#FFEF6F'},
            {'name': '501-600', 'value': 423992200, 'color': '#F26D5B'},
            {'name': '601-700', 'value': 229992200, 'color': '#C03546'},
            {'name': '701-800', 'value': 623992200, 'color': '#492540'},
        ],
        kyc_drilldown=[
            {'name': 'Verified', 'value': 770, 'color': '#60316E'},
            {'name': 'No Identity', 'value': 70, 'color': '#4B6289'},
            {'name': 'Currently Delinquent', 'value': 190, 'color': '#29A19C'},
            {'name': 'Historically Delinquent', 'value': 260, 'color': '#A3F7BF'},
        ]
    )

    return TemplateResponse(request, "risk_management/dashboard.html", context)

def portfolio_at_risk(request):
    context = {}
    return TemplateResponse(request, "risk_management/portfolio_at_risk.html", context)
