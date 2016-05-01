from django.db.models import Q, Sum, F

from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction as db_transaction, IntegrityError

from ..utils import get_reference_no, record_log

import logging
from decimal import Decimal as D

from ..models import *

INITIAL = D('0.0')

def get_net_balance(entries):
    #Aggregate the ledger balance increment column
    ledger_balance = entries.aggregate(
        ledger_balance=Sum('ledger_balance_increment')
    )
    #aggregate returns a dictionary above, pop using the key
    ledger_balance = ledger_balance.pop('ledger_balance')

    #return the ledger balance
    return (ledger_balance or INITIAL)

#-------------------------------------------------------------

def get_pending_entries_net_balance(
    ledger_account, 
    product_account=None,
    product_type=LedgerTransactionBlockItem.LOAN,
    start_date=None, 
    end_date=None
):
    entries = get_ledger_entries(
        ledger_account,
        product_account=product_account,
        product_type=product_type,
        start_date=start_date,
        end_date=end_date,
        status_code=PENDING_POSTING
    )
    return get_net_balance(entries)

def get_posted_entries_net_balance(
    ledger_account, 
    product_account=None,
    product_type=LedgerTransactionBlockItem.LOAN,
    start_date=None, 
    end_date=None
):
    entries = get_ledger_entries(
        ledger_account,
        product_account=product_account,
        product_type=product_type,
        start_date=start_date,
        end_date=end_date,
        status_code=POSTED
    )
    return get_net_balance(entries)

#-------------------------------------------------------------

def get_ledger_entries(
    ledger_account, 
    product_account=None,
    product_type=LedgerTransactionBlockItem.LOAN,
    entries=None, 
    start_date=None, 
    end_date=None,
    status_code=None
):
    '''
    Product accounts are different from General Accounts.
    For product accounts, pending entries
    '''
    if not entries:
        entries = LedgerEntry.objects.filter(ledger_account=ledger_account)
    else:
        entries = entries.filter(ledger_account=ledger_account)

    if status_code:
        entries = entries.filter(ledger_transaction__last_status__code=status_code)
    
    if product_account:
        entries = entries.filter(product_account=product_account, product_type=product_type)

    # if start_date is not None:
    #     entries = entries.filter(ledger_transaction__last_status_date__gte=start_date)

    # if end_date is None:
    #     end_date = timezone.now()

    # entries = entries.filter(ledger_transaction__last_status_date__lt=end_date)

    return entries

