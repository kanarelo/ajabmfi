from django.db.models import Q, Sum, F
from django.utils import timezone

from decimal import Decimal as D

import uuid

from calendar import monthrange
from datetime import timedelta

from ...core.facades import *
from .loan_transactions import *

INITIAL = D('0.0')

def get_gross_loan_portfolio(user):
    """
    All outstanding principal for all outstanding client loans, including current, 
    delinquent and restructured loans, but not loans that have been written off
    """
    loans = LoanAccount.objects.active()
    loans = loans.aggregate(
        total_current_balance=Sum('last_current_balance')
    )
    return loans['total_current_balance']

def get_net_loan_portfolio(user):
    """Gross Loan Portfolio minus Loan Loss Reserve"""
    return get_gross_loan_portfolio(user) - get_provision_for_bad_debt()

def get_provision_for_bad_debt(user):
    """
    The portion of the gross loan portfolio that has been expensed
    in anticipation of losses due to default.
    """
    PROVISION_FOR_BAD_DEBT_GL_CODE = "1.4300.0000"

    balance_amount = get_last_closing_balance(PROVISION_FOR_BAD_DEBT_GL_CODE)

    return balance_amount
