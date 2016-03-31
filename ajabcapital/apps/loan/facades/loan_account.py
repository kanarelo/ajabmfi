from django.db.models import Q, Sum, F
from django.utils import timezone

from decimal import Decimal as D

import uuid

from calendar import monthrange
from datetime import timedelta

from ...core.facades import *

from .loan_transactions import *

INITIAL = D('0.0')

def next_repayment_date(loan):
    if loan.repayment_model.code == "TRM_001": #term
        # term = loan.
        pass
    elif loan.repayment_model.code == "TRM_002":
        pass

def next_principal_repayment():
    pass

def next_possible_account_statuses(status):
    if status is None:
        return None

    if status.code == "":
        pass
0
def get_loan_account_current_balance(loan_account):
    accounts = get_chart_of_accounts_balances(loan_account, 
        filter_accounts=['portfolio_control_account']
    )
    return accounts['portfolio_control_account']['balance']

def get_repayment_due_on_loan_account(loan_account):
    accruals_due_on_account  = get_accruals_due_on_loan_account(loan_account)
    principal_due_on_account = get_principal_due_on_loan_account(loan_account)

    return (
        INITIAL + 
        accruals_due_on_account + 
        principal_due_on_account 
    )

def get_accruals_due_on_loan_account(loan_account):
    accounts = get_chart_of_accounts_balances(
        loan_account, filter_accounts=[
            'interest_income_receivable_account',
            'fee_income_receivable_account',
            'penalty_income_receivable_account'
        ]
    )
    return (
        accounts['fee_income_receivable_account']['balance'] +
        accounts['interest_income_receivable_account']['balance'] +
        accounts['penalty_income_receivable_account']['balance'] 
    )

def get_fees_due_on_loan_account(loan_account):
    accounts = get_chart_of_accounts_balances(
        loan_account, filter_accounts=['fee_income_receivable_account']
    )
    return accounts['fee_income_receivable_account']['balance']

def get_penalties_due_on_loan_account(loan_account):
    accounts = get_chart_of_accounts_balances(
        loan_account, filter_accounts=['penalty_income_receivable_account']
    )
    return accounts['penalty_income_receivable_account']['balance']

def get_interest_due_on_loan_account(loan_account):
    accounts = get_chart_of_accounts_balances(
        loan_account, filter_accounts=['interest_income_receivable_account']
    )
    return accounts['interest_income_receivable_account']['balance']

def get_principal_due_on_loan_account(loan_account):
    return D('0.0')
