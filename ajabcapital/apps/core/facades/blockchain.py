from django.db.models import Q, Sum, F, Max, Min

from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction as db_transaction, IntegrityError

from ..utils import get_reference_no, record_log

import logging
from decimal import Decimal as D

from ..models import *
from .accounting import *

INITIAL = D('0.0')

#-------------------------------------------------------------

PENDING_POSTING = "LTS_001"
POSTED = "LTS_002"

#-------------------------------------------------------------

def get_balance_carried_forward(
    ledger_account, 
    product_account=None, 
    product_type=LedgerTransactionBlockItem.LOAN
):
    try:
        latest_block = LedgerTransactionBlock.objects.latest('balances_as_at')
        ledger_account_block_items = latest_block.block_items.filter(
            ledger_account=ledger_account
        )

        if product_account:
            ledger_account_block_items = ledger_account_block_items.filter(
                product_account=product_account,
                product_type=product_type
            )

        ledger_account_block_item = ledger_account_block_items.get()

        #get the balance amount
        last_balance_amount = ledger_account_block_item.balance_amount
        last_balance_date   = latest_block.balances_as_at
    except ObjectDoesNotExist:
        last_balance_amount = D('0.0')
        last_balance_date   = LedgerTransaction.objects.aggregate(
            min_created_at=Min('created_at')
        ).pop('min_created_at', timezone.now())

    return (last_balance_amount, last_balance_date)

#-------------------------------------------------------------

def get_ledger_account_balance(
    ledger_account, 
    product_account=None,
    product_type=LedgerTransactionBlockItem.LOAN
):
    
    balance_cf, balance_as_at = get_balance_carried_forward(ledger_account)

    pending_balance = get_pending_entries_net_balance(
        ledger_account, 
        product_account=product_account,
        product_type=product_type,
        start_date=balance_as_at
    )

    return (balance_cf + pending_balance)

def update_account_levels(ledger_accounts):
    ledger_accounts_list = []
    for ledger_account in ledger_accounts:
        ledger_accounts_list.append(
            update_account_level(ledger_account)
        )
    return ledger_accounts_list

def update_account_level(ledger_account):
    previous_ledger_code = 0

    #get the ledger code
    ledger_code = ledger_account.ledger_code

    (factor, no_of_zeros) = (8, ledger_code.count('0'))
    
    level = (factor - no_of_zeros)

    ledger_account.ledger_level = level

    return ledger_account

def update_account_balance(ledger_account):
    ledger_account.balance = get_ledger_account_balance(ledger_account)

    return ledger_account

def update_account_balances(ledger_accounts):
    ledger_accounts_list = []
    for ledger_account in ledger_accounts:
        ledger_accounts_list.append(
            update_account_balance(ledger_account)
        )
    return ledger_accounts_list

def update_account_details(ledger_accounts):
    ledger_accounts = update_account_levels(ledger_accounts)
    ledger_accounts = update_account_balances(ledger_accounts)

    return ledger_accounts

def p():
    def get_int_code(ledger_code):
        ledger_code = int(ledger_code.replace(".", ""))
        return ledger_code

    (a, b, c) = (0, 0, 0)
    d = []

    NODE_TYPE_ROOT = 1
    NODE_TYPE_PARENT = 2
    NODE_TYPE_CHILD = 3
    NODE_TYPE_SIBLING = 3

    ledger_accounts = LedgerAccount.objects.all().order_by(
        'ledger_code'
    )

    accounts = []
    
    for outer in ledger_accounts:
        outer = update_account_level(outer)

        outer.children = []
        outer.siblings = []

        for inner in ledger_accounts:
            if inner == outer:
                continue

            if not (inner.account_category == outer.account_category): 
                continue

            inner = update_account_level(inner)

            is_child = (
                #1.0000.0000 and 1.1000.0000
                #1.1000.0000 and 1.1100.0000
                inner.ledger_level == (outer.ledger_level + 1)
            ) and (
                inner.ledger_code > outer.ledger_code
            ) and (
                inner.ledger_code <= outer.ledger_code.replace("0", "9")
            )

            is_sibling = (
                #1.0000.0000 and 2.0000.0000
                #1.1000.0000 and 1.2000.0000
                inner.ledger_level == outer.ledger_level
            ) and (
                inner.ledger_code > outer.ledger_code
            )

            is_not_related = (
                #1.1000.0000 and 2.0000.0000
                #1.2100.0000 and 1.3000.0000
                inner.ledger_level < outer.ledger_level
            ) and (
                inner.ledger_code > outer.ledger_code
            )

            if is_not_related:
                break
            elif is_child:
                outer.children.append(inner)
            elif is_sibling:
                outer.siblings.append(inner)

        if outer.ledger_level == 0:
            accounts.append(outer)

    def print_account(account):
        print ("\t" * account.ledger_level), account
        [print_account(child) for child in account.children]

    [print_account(account) for account in accounts]


#-------------------------------------------------------------

def close_ledger_account(
    ledger_account, 
    block, 
    product_account=None, 
    product_type=LedgerTransactionBlockItem.LOAN, 
    user=None
):
    def create_block_item(block, balance_amount, ledger_account):
        return LedgerTransactionBlockItem.objects.create(
            block=block,
            balance_amount=balance_amount,
            ledger_account=ledger_account,
            product_account=product_account,
            created_by=user
        )

    def do_post_pending_entries(entries):
        for entry in entries:
            ledger_transaction = entry.ledger_transaction
            
            if ledger_transaction.last_status.code == PENDING_POSTING:
                status = update_transaction_status(
                    ledger_transaction, 
                    POSTED, 
                    user, 
                    "Automatic closure at end of business day", 
                    status_date=None
                )

    #The Algorithm
    with db_transaction.atomic():
        balance_amount = get_ledger_account_balance(
            ledger_account, 
            product_account=product_account,
            product_type=product_type
        )

        #create block item
        block_item = create_block_item(block, balance_amount, ledger_account)

        #post all the pending entries to the ledger
        do_post_pending_entries(post_pending_entries)

        return block_item
