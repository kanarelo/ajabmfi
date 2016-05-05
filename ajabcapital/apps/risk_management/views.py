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

from .models import *
from ..loan.models import LoanProfile

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
        expected_loss="500m",
        expected_loss_percentage=40,
        risk_weighted_assets=1428992999,
        exposure_at_default="1.4b",
        npl_by_credit_rating=[
            {'name': '200-300', 'value': 223992200, 'color': '#492540'},
            {'name': '301-400', 'value': 123992200, 'color': '#C03546'},
            {'name': '401-500', 'value': 223992200, 'color': '#F26D5B'},
            {'name': '501-600', 'value': 423992200, 'color': '#FFEF6F'},
            {'name': '601-700', 'value': 229992200, 'color': '#F6EA8C'},
            {'name': '701-800', 'value': 623992200, 'color': '#EFF2DD'},
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

def kyc(request):
    loan_profiles = LoanProfile.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(loan_profiles, request.GET.get('count', 12)) # Show 11 contacts per page

    try:
        loan_profiles = paginator.page(page)
    except PageNotAnInteger:
        loan_profiles = paginator.page(1)
    except EmptyPage:
        loan_profiles = paginator.page(paginator.num_pages)

    context = dict(
        loan_profiles=loan_profiles
    )
    return TemplateResponse(request, "risk_management/kyc.html", context)

def watch_list(request):
    loan_profiles = LoanProfile.objects.filter(
        Q(individual_profile__identity_number__isnull=False)|
        Q(business_profile__identity_number__isnull=False)
    ).order_by('created_at')
    page = request.GET.get('page', 1)
    paginator = Paginator(loan_profiles, request.GET.get('count', 12)) # Show 11 contacts per page


    try:
        loan_profiles = paginator.page(page)
    except PageNotAnInteger:
        loan_profiles = paginator.page(1)
    except EmptyPage:
        loan_profiles = paginator.page(paginator.num_pages)

    for loan_profile in loan_profiles:
        loan_profile.credit_score = random.randint(200, 500)
        loan_profile.credit_score_down_percentage = random.randint(5, 50)

        try:
            loan_profile.risk_profile.has_current_delinquency = random.choice([True, False])
            loan_profile.risk_profile.has_historical_delinquency = random.choice([True, False])
        except ObjectDoesNotExist:
            class D:
                pass
            loan_profile.risk_profile = RiskProfile()
            loan_profile.risk_profile.is_verified = True, False
            loan_profile.risk_profile.has_fraud = random.choice([True, False])
            loan_profile.risk_profile.has_current_delinquency = random.choice([True, False])
            loan_profile.risk_profile.has_historical_delinquency = random.choice([True, False])
            loan_profile.days_in_arrears = random.choice([0,30,23,35,90,130,139,46,83,92,180,237])

    context = dict(
        loan_profiles=loan_profiles
    )
    return TemplateResponse(request, "risk_management/watch-list.html", context)

def liquidity(request):
    context = {}
    return TemplateResponse(request, "risk_management/liquidity.html", context)

def policies(request):
    context = {}
    return TemplateResponse(request, "risk_management/policies.html", context)

def crb_settings(request):
    context = {}
    return TemplateResponse(request, "risk_management/crb_settings.html", context)
