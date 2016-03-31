from django.db.models import Q, Sum, F
from django.utils import timezone

from decimal import Decimal as D

import uuid

from calendar import monthrange
from datetime import timedelta

from ajabcapital.apps.core.facades import *
from .loan_transactions import *

INITIAL = D('0.0')

def get_loan_overdues_by_product():
    pass

def get_loan_current_balances_by_gender():
    pass

def get_loan_current_balances_by_product():
    pass

def get_loan_current_balances_by_product_type():
    pass

def get_loan_balances_by_risk_by_level():
    pass

def get_loan_funds_drawdown_trends():
    pass

def get_loan_funds_repayment_trends():
    pass
