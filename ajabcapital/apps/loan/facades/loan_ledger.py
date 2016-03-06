from django.db.models import Q, Sum, F
from django.utils import timezone

from decimal import Decimal as D

import uuid

from calendar import monthrange
from datetime import timedelta

from ajabcapital.apps.core.facades import *
from .loan_transactions import *

INITIAL = D('0.0')

def get_loan_account_current_balance(loan_account):
    accounts = get_chart_of_accounts_balances(loan_account, 
        filter_accounts=['portfolio_control_account']
    )
    return accounts['portfolio_control_account']['balance']

def get_loan_repayment_due(loan_account):
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

#Ledger Balances
#---------------------------
def get_general_ledger_balance(ledger_account, loan_account=None, start_date=None, end_date=None):
    coa = LoanChartOfAccounts.objects.get()

    if loan_account:
        return get_product_ledger_balance(loan_account, ledger_account, start_date=start_date, end_date=end_date)

    return get_ledger_account_balance(ledger_account, start_date=start_date, end_date=end_date)

def get_chart_of_accounts_balances(loan_account=None, filter_accounts=[]):
    coa = LoanChartOfAccounts.objects.get()
    
    accounts = dict(
        portfolio_control_account=dict(account=coa.loan_portfolio_control_account, balance=D('0.0')),
        funding_source_account=dict(account=coa.loan_funding_source_account, balance=D('0.0')),
        interest_income_receivable_account=dict(account=coa.loan_interest_income_receivable_account, balance=D('0.0')),
        interest_income_account=dict(account=coa.loan_interest_income_account, balance=D('0.0')),
        fee_income_receivable_account=dict(account=coa.loan_fee_income_receivable_account, balance=D('0.0')),
        fee_income_account=dict(account=coa.loan_fee_income_account, balance=D('0.0')),
        penalty_income_receivable_account=dict(account=coa.loan_penalty_income_receivable_account, balance=D('0.0')),
        penalty_income_account=dict(account=coa.loan_penalty_income_account, balance=D('0.0')),
        principal_write_off_expense_account=dict(account=coa.loan_principal_write_off_expense_account, balance=D('0.0')),
        interest_write_off_expense_account=dict(account=coa.loan_interest_write_off_expense_account, balance=D('0.0')),
        penalty_write_off_expense_account=dict(account=coa.loan_penalty_write_off_expense_account, balance=D('0.0')),
        fee_write_off_expense_account=dict(account=coa.loan_fee_write_off_expense_account, balance=D('0.0'))
    )
    
    for k, v in accounts.iteritems():
        for account in filter_accounts:
            if account == k:
                accounts[k]['balance'] = get_general_ledger_balance(v['account'], loan_account=loan_account)

    return accounts
