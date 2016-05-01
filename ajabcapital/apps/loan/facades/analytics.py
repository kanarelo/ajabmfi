from django.db.models import Q, Sum, F
from django.utils import timezone

from decimal import Decimal as D

import uuid

from calendar import monthrange
from datetime import timedelta

from ajabcapital.apps.core.facades import *
from .loan_transactions import *

from ...risk_management.models import *

INITIAL = D('0.0')

def get_loan_overdues_by_product():
    pass

def get_loan_current_balances_by_gender():
    pass

def get_loan_current_balances_by_product():
    pass

def get_loan_current_balances_by_product_type():
    pass

def get_portfolio_by_product():
    products = LoanProduct.objects.all()
    active_loans = LoanAccount.objects.active()

    for product in products:
        product.value = active_loans.filter(
            product=product
        ).aggregate(
            total_current_balance=Sum('current_balance')
        ).pop('total_current_balance') or INITIAL

    return products

def get_portfolio_by_risk_by_level():
    classifications = ConfigLoanRiskClassification.objects.filter(
        is_active=True
    ).order_by('code')
    loans = LoanAccount.objects.all()
    
    for classification in classifications:
        classified_loans = loans.risk_classified(
            classification.code
        )
        classification.value = classified_loans.aggregate(
            total_current_balance=Sum('current_balance')
        ).pop('total_current_balance') or INITIAL

    return classifications


def get_loan_funds_drawdown_trends():
    pass

def get_loan_funds_repayment_trends():
    pass
