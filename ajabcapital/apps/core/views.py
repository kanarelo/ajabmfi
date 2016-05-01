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

from decimal import Decimal as D

from . import forms, facades
from . import (utils as core_utils, forms as core_forms)
from ..loan import facades as loan_facades
from ..risk_management.models import *

@login_required
def dashboard(request):
    user = request.user

    context = {
        'gross_non_performing_loans': loan_facades.gross_non_performing_loans(),
        'gross_loan_portfolio': loan_facades.get_gross_loan_portfolio(),
        'provision_for_bad_debt': loan_facades.get_provision_for_bad_debt(),
        'net_loan_portfolio': loan_facades.get_net_loan_portfolio(),
        'par': {
            'Normal (PAR = 0)': D('0.0'),
            'Standard (PAR < 30)': D('0.0'),
            'Watch (PAR >= 31)': D('0.0'),
            'Substandard (PAR >= 61)': D('0.0'),
            'Doubtful (PAR >= 91)': D('0.0'),
            'Loss (PAR >= 181)': D('0.0'),
        },
        'pipeline_items': [
            {'name': 'Application', 'amount': D('453.0'), 'percentage': D('40.91') * 2, "background_color": "#1F3A52", "color": "#fff"},
            {'name': 'Credit Analysis', 'amount': D('240.0'), 'percentage': D('27.27') * 2, "background_color": "#41A186", "color": "#fff"},
            {'name': 'Risk Analysis', 'amount': D('153.0'), 'percentage': D('18.18') * 2, "background_color": "#7ebf5d", "color": "#000"},
            {'name': 'Processing', 'amount': D('110.0'), 'percentage': D('9.09') * 2, "background_color": "#b5e09f", "color": "#000"},
            {'name': 'Disbursement', 'amount': D('60.0'), 'percentage': D('4.55') * 2, "background_color": "#D3F689", "color": "#000"},
        ],
        'portfolio_by_risk': loan_facades.get_portfolio_by_risk_by_level(),
        'portfolio_by_product':loan_facades.get_portfolio_by_product(),
        'average_loan_balance': loan_facades.get_average_loan_balance(),
        'women_borrowers': loan_facades.get_women_borrowers(),
        'active_borrowers': loan_facades.get_active_borrowers(),
        'women_borrowers_percentage': loan_facades.get_women_borrowers_percentage(),
        'asset_to_equity_ratio': D('2.63') * D('100.0'),
        'debt_to_equity_ratio': D('0.978') * D('100.0'),
        'risk_coverage_ratio': loan_facades.get_risk_coverage_ratio() * D('100.0'),
    }
    
    return TemplateResponse(request, "core/dashboard.html", context)

@login_required
def main_menu(request):
    return TemplateResponse(request, "core/main_menu.html", {

    })

@login_required
def notifications(request):
    return TemplateResponse(request, "core/notifications.html", {

    })
