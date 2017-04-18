from django.db.models import Q, Sum, F, Avg
from django.utils import timezone

from decimal import Decimal as D

import uuid

from calendar import monthrange
from datetime import timedelta

from ...core.facades import *
from ...risk_management.facades import *
from .loan_transactions import *

INITIAL = D('0.0')

GROSS_LOAN_PORTFOLIO_GL_CODE   = "1.4100.0000"
PROVISION_FOR_BAD_DEBT_GL_CODE = "1.4300.0000"

def get_business_borrowers():
    return D(LoanProfile.objects.business_profiles().count())

def get_group_borrowers():
    return D(LoanProfile.objects.group_profiles().count())

def get_active_borrowers():
    return D(LoanProfile.objects.all().count())

def get_women_borrowers():
    return D(LoanProfile.objects.women_profiles().count())

def get_women_borrowers_percentage():
    active_borrowers = get_active_borrowers()
    if active_borrowers <= 0:
        return 0

    return (
        get_women_borrowers() / active_borrowers
    ) * 100

def get_average_loan_balance():
    return LoanAccount.objects.performing().aggregate(
        total_current_balance=Avg('current_balance')
    ).pop('total_current_balance') or INITIAL

def get_risk_coverage_ratio():
    _gross_non_performing_loans = gross_non_performing_loans()
    if _gross_non_performing_loans <= 0:
        return 0

    return (
        get_provision_for_bad_debt() / _gross_non_performing_loans
    )

def gross_non_performing_loans():
    total_current_balance = INITIAL
    non_perfoming_loans = LoanAccount.objects.non_performing()

    classifications = ConfigLoanRiskClassification.objects.filter(
        is_active=True
    ).filter(
        code__gte="LRC_003"
    )
    
    for classification in classifications:
        #get active loans
        #limit classified loans
        classified_loans = non_perfoming_loans.risk_classified(
            classification.code
        )
        current_balance_sum = classified_loans.aggregate(
            total_current_balance=Sum('current_balance')
        ).pop('total_current_balance') or INITIAL

        #add to the `total_current_balance`
        total_current_balance += current_balance_sum

    return total_current_balance

def get_gross_loan_portfolio():
    """
    All outstanding principal for all outstanding client loans, including current, 
    delinquent and restructured loans, but not loans that have been written off
    """
    # ledger_account = LedgerAccount.objects.get(ledger_code=GROSS_LOAN_PORTFOLIO_GL_CODE)
    # balance_amount = get_ledger_account_balance(ledger_account)
    # return balance_amount

    active_loans = LoanAccount.objects.active()

    total_current_balance = active_loans.aggregate(
        total_current_balance=Sum('current_balance')
    ).pop('total_current_balance') or INITIAL

    return total_current_balance

def get_provision_for_bad_debt():
    """
    The portion of the gross loan portfolio that has been expensed
    in anticipation of losses due to default.
    """
    total_current_balance = INITIAL
    active_loans = LoanAccount.objects.active()

    classifications = ConfigLoanRiskClassification.objects.filter(is_active=True)
    
    for classification in classifications:
        #get active loans
        #limit classified loans
        classified_loans = active_loans.risk_classified(
            classification.code
        )
        current_balance = classified_loans.aggregate(
            total_current_balance=Sum('current_balance')
        ).pop('total_current_balance') or INITIAL

        #provisioned amount
        provision_amount = (
            current_balance * (
                classification.default_provision / D('100.00')
            )
        )
        #accrue the value
        total_current_balance += provision_amount

    return total_current_balance

def get_net_loan_portfolio():
    """Gross Loan Portfolio minus Loan Loss Reserve"""
    return get_gross_loan_portfolio() - get_provision_for_bad_debt()
