from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse

from django.http import (
    HttpResponseRedirect, 
    Http404, 
    JsonResponse, 
    HttpResponseForbidden, 
    HttpResponse
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
    forms as core_forms,
    facades as core_facades
)
from ..core.models import *

@login_required
def dashboard(request):
    user = request.user

    context = dict(
        quick_accounts=facades.get_quick_accounts(user),
        net_loan_portfolio=facades.get_net_loan_portfolio(user),
        gross_loan_portfolio=facades.get_gross_loan_portfolio(user),
        provision_for_bad_debt=facades.get_portfolio_at_risk_by_level(user),
        key_perfomance_indicators=facades.get_key_perfomance_indicators(user),
        return_on_assets=143,
        gross_margin_ratio=26,
        working_capital_ratio=16020121.99,
        liquidity_ratio=129,
        asset_breakdown=[
            {'name': 'Cash', 'value': 84474367.86, 'color': "#26252C"},
            {'name': 'Financial Investments', 'value': 4909999.23, 'color': "#E54861"},
            {'name': 'Net Loan Portfolio', 'value': 1238453244.04, 'color': "#F2A379"},
            {'name': 'Net Fixed Assets', 'value': 2109002.23, 'color': "#E0B58C"},
            {'name': 'Accounts Receivable', 'value': 7891212.23, 'color': "#EFD5B7"},
        ],
        expense_breakdown=[
            {'name': 'Financial Expense', 'value': 16899902.89, 'color': "#5D414D"},
            {'name': 'Operating Expense', 'value': 33788789.91, 'color': "#7E858B"},
            {'name': 'Administrative Expense', 'value': 1233220.12, 'color': "#ABD4C1"},
        ],
    )

    return TemplateResponse(request, "accounting/dashboard.html", context)

@login_required
def general_journal(request):
    entries = LedgerEntry.objects.all().order_by('-created_at')

    page = request.GET.get('page', 1)
    paginator = Paginator(entries, request.GET.get('count', 12)) # Show 11 contacts per page

    try:
        entries = paginator.page(page)
    except PageNotAnInteger:
        entries = paginator.page(1)
    except EmptyPage:
        entries = paginator.page(paginator.num_pages)

    return TemplateResponse(request, "accounting/general_journal.html", {
        'entries': entries
    })

@login_required
def balance_sheet(request):
    balance_sheet = {
        'assets': {
            'current_assets': core_facades.update_account_levels(
                LedgerAccount.objects.asset()
            ),
            'fixed_assets': [],
        },
        'liabilities': {
            'current_liabilities': core_facades.update_account_levels(
                LedgerAccount.objects.liability()
            )
        },
        'equity': core_facades.update_account_levels(LedgerAccount.objects.equity())
    }

    return TemplateResponse(request, "accounting/balance_sheet.html", {
        'balance_sheet': balance_sheet
    })

@login_required
def pnl_statement(request):
    pnl_statement = {
        'income': core_facades.update_account_levels(
            LedgerAccount.objects.income()
        ),
        'expense': core_facades.update_account_levels(
            LedgerAccount.objects.expense()
        ),
    }

    return TemplateResponse(request, "accounting/pnl_statement.html", {
        'balance_sheet': pnl_statement
    })

@login_required
def trial_balance(request):
    trial_balance = {
        'assets': {
            'current_assets': core_facades.update_account_levels(
                LedgerAccount.objects.asset()
            ),
            'fixed_assets': [],
        },
        'liabilities': {
            'current_liabilities': core_facades.update_account_levels(
                LedgerAccount.objects.liability()
            )
        },
        'equity': core_facades.update_account_levels(
            LedgerAccount.objects.equity()
        ),
        'income': core_facades.update_account_levels(
            LedgerAccount.objects.income()
        ),
        'expense': core_facades.update_account_levels(
            LedgerAccount.objects.expense()
        )
    }

    return TemplateResponse(request, "accounting/trial_balance.html", {
        'trial_balance': trial_balance
    })

@login_required
def product_ledgers(request):
    product_ledgers = {}

    return TemplateResponse(request, "accounting/product_ledgers.html", {
        'product_ledgers': product_ledgers
    })

@login_required
def banking(request):
    banking = {}

    return TemplateResponse(request, "accounting/banking.html", {
        'banking': banking
    })