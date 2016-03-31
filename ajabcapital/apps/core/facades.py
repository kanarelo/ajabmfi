from django.db.models import Q, Sum, F

from django.utils import timezone
from django.db import transaction as db_transaction, IntegrityError

from .utils import get_reference_no, record_log

import logging
from decimal import Decimal as D

from .models import *
from ..loan.facades import *

INITIAL = D('0.0')

#-----------------------------

def get_sum_of_transaction_items(entries):
    #Aggregate the ledger balance increment column
    ledger_balance = entries.aggregate(
        ledger_balance=Sum('ledger_balance_increment')
    )
    #aggregate returns a dictionary above, pop using the key
    ledger_balance = ledger_balance.pop('ledger_balance')

    #return the ledger balance
    return ledger_balance or INITIAL

def get_ledger_account_balance(ledger_account, start_date=None, end_date=None):
    entries = LedgerEntry.objects.filter(ledger_account=ledger_account)

    if start_date is not None:
        entries = entries.filter(last_status__gte=start_date)

    if end_date is not None:
        entries = entries.filter(last_status__lt=end_date)

    return get_sum_of_transaction_items(entries)

def get_product_ledger_balance(
    product_account, ledger_account,
    start_date=None, end_date=None
):
    entries = LedgerEntry.objects.filter(
        ledger_account=ledger_account,
        product_account=product_account.account_number
    )

    if start_date is not None:
        entries = entries.filter(last_status__gte=start_date)

    if end_date is not None:
        entries = entries.filter(last_status__lt=end_date)

    return get_sum_of_transaction_items(entries)

#----------------------------------------------------------

def get_last_closing_balance(ledger_account):
    # last_closing_block_item = BlockItem
    #last_closing_block_item.balance_amount
    return 0

#----------------------------------------------------------

def get_transaction_type_account_turple(transaction_type):
    accounting_rule = LedgerAccountingRule.objects.get(
        transaction_type=transaction_type
    )
    return (
        accounting_rule.debit_account, 
        accounting_rule.credit_account
    )

def get_ledger_balance_increment(amount, account, item_type):
    #constants
    ASSET = "1"
    LIABILITY = "2"
    EQUITY = "3"
    INCOME = "4"
    EXPENSE = "5"

    if (amount is None) or (not amount):
        raise Exception("Invalid amount")

    if account.account_category.code in (ASSET, EXPENSE):
        #Assets and expenses increase with debit
        if (item_type == LedgerTransactionEntry.DEBIT):
            amount = +(amount)
        #Yet they decrease with credits
        elif (item_type == LedgerTransactionEntry.CREDIT):
            amount = -(amount)
    elif account.account_category.code in (LIABILITY, EQUITY, INCOME):
        #Liability, Equity and Income accounts decrease with debits
        if (item_type == LedgerTransactionEntry.DEBIT): 
            amount = -(amount)
        #Yet they increase with credits
        elif (item_type == LedgerTransactionEntry.CREDIT):
            amount = +(amount)
    else:
        #if the account is faulty, dont pass through
        return

    #constants
    NORMAL_ACCOUNT = "1"
    CONTRA_ACCOUNT = "2"

    account_type_code = account.account_type.code

    #normal account
    if account_type_code == NORMAL_ACCOUNT:
        #for normal accounts, return amount as it is by this point
        return amount
    elif account_type_code == CONTRA_ACCOUNT:
        #a contra account is a general ledger account which is intended 
        #to have its balance be the opposite of the normal balance for 
        #that account classification
        #In that case, lets negate the balance, so that we can get its opposite
        return -(amount)

#------------------------------------------
def close_ledger_accounts():
    GENERAL_LEDGER = "LGT_001"
    DETAIL_ACCOUNT = "LAT_002"

    # We are only interested in accounts listed as part 
    # of the general ledger, anything else will be sorted by a different engine
    # also. make sure uts a detail account and its active...
    # Detail accounts will be included in the Balance closures as their balances are 
    ledger_accounts = LedgerAccount.objects.filter(
        ledger_type__code=GENERAL_LEDGER,
        account_type__code=DETAIL_ACCOUNT,
        is_active=True
    ).order_by('ledger_code')

    #Loop through the ledger accounts
    for ledger_account in ledger_accounts:
        close_ledger_account(ledger_account)

def close_ledger_account(ledger_account):
    POSTED = "LTS_002"
    GL_BLOCK = "BC_001"

    time_closed = timezone.now()

    def get_next_block():
        return LedgerTransactionBlock.objects.create(
            name="%s @ %s" % (automatic_balance_closure_type.name, time_closed),
            notes="%s @ %s" % (automatic_balance_closure_type.name, time_closed),
            balance_closure_type=automatic_balance_closure_type,
            balances_as_at=time_closed,
        )

    def get_previous_balance_and_date():
        block_type = ConfigBlockType.objects.get(code=GL_BLOCK)

        try:
            previous_block = LedgerTransactionBlock.objects.filter(
                block_type=block_type
            ).latest('balances_as_at')
            block_item = previous_block.items.filter(
                ledger_account=ledger_account
            ).latest('balance_closure__balance_as_at')

            #get the balance amount
            last_balance_amount = block_item.balance_amount
            last_balance_date   = previous_block.balances_as_at
        except LedgerTransactionBlock.DoesNotExist:
            last_balance_amount = D('0.0')
            last_balance_date = None

        return (last_balance_amount, last_balance_date)

    def get_entries_accrued(from_date, to_date):
        #create the filter logic
        filter_logic = Q(ledger_account=ledger_account) 
        #get only entries from posted transactions
        filter_logic &= Q(ledger_transaction__last_status__code=POSTED)

        #if the last balance balance date is known, lets use it, else we will accrue from start
        if last_balance_date is not None:
            filter_logic |= Q(
                ledger_transaction__last_status_date__gte=from_date,
                ledger_transaction__last_status_date__lt=to_date
            )
        return LedgerEntry.objects.filter(filter_logic)

    def create_block_item(balance_closure, balance_amount, ledger_account):
        return LedgerTransactionBlockItem.objects.create(
            balance_closure=balance_closure,
            balance_amount=new_balance_amount,
            ledger_account=ledger_account
        )

    #The Algorithm
    with db_transaction.atomic():
        cut_off_time = timezone.now()
        #Get the previous balances
        (last_balance_amount, last_balance_date) = get_previous_balance_and_date()

        #create the next balance closure for this call
        next_block = get_next_block()

        #get all the entried accrued since last balance date
        entries_accrued = get_entries_accrued(last_balance_date)
        #get latest balance amount
        balance_amount  = get_sum_of_transaction_items(entries_accrued)
        #get the new balance amount: previous balance + latest accrued balances
        new_balance_amount = (last_balance_amount + balance_amount)

        #create block item
        block_item = create_block_item(next_block, new_balance_amount, ledger_account)
        return balance_closure_item

#-------------------------------------    
def create_transaction(
    transaction_type=None, credit_account=None, debit_account=None, currency=None,
    product_account=None, amount=None, status=None, user=None, notes=None, reversing_transaction=None,
    *args, **kwargs
):
    if not (
        (amount and currency) and 
        (user) and
        (transaction_type and notes) and
        (credit_account and debit_account)
    ):
        raise Exception("please provide valid parameters for this transaction.")

    def create_transaction_obj():
        #get the transaction number
        PENDING_POSTING = 2
        transaction_no = get_reference_no()

        if not LedgerTransaction.objects.filter(
            transaction_no=transaction_no
        ).exists():
            transaction = LedgerTransaction.objects.create(
                transaction_type=transaction_type,
                status_id=(status or PENDING_POSTING),
                transaction_no=transaction_no,
                product_account=product_account.account_number,
                reversing_transaction=reversing_transaction,
                currency=currency,
                amount=amount,
                notes=notes,
                created_by=user
            )
            record_log(
                credit_account=credit_account.ledger_code,
                debit_account=debit_account.ledger_code,
                transaction_type=transaction_type.code,
                product_account=product_account.account_number,
                reversing_transaction=reversing_transaction,
                transaction_no=transaction_no,
                status=(status or PENDING_POSTING),
                amount=amount,
                currency=currency,
                user=user,
                **kwargs
            )
            return transaction
        else:
            return create_transaction_obj()

    def create_transaction_entry(transaction, ledger_account, item_type, increment):
        #Adds debit entry for transaction
        return LedgerEntry.objects.create(
            ledger_balance_item_type=item_type,
            ledger_balance_increment=increment,
            ledger_transaction=transaction,
            product_account=transaction.product_account,
            ledger_account=ledger_account,
            created_by=user,
        )

    with db_transaction.atomic():
        transaction = create_transaction_obj()

        #get the debit and credit ledger balance increments to use for the entries
        debit_ledger_balance_increment = get_ledger_balance_increment(
            amount, debit_account, LedgerTransactionEntry.DEBIT
        )
        credit_ledger_balance_increment = get_ledger_balance_increment(
            amount, credit_account, LedgerTransactionEntry.CREDIT
        )

        if (debit_ledger_balance_increment and credit_ledger_balance_increment):
            #Adds credit entry for transaction
            debit_entry  = create_transaction_entry(
                transaction, debit_account,  
                LedgerTransactionEntry.DEBIT, 
                debit_ledger_balance_increment
            )
            credit_entry = create_transaction_entry(
                transaction, credit_account, 
                LedgerTransactionEntry.CREDIT, 
                credit_ledger_balance_increment
            )

            return (debit_entry, credit_entry)

        return (None, None)

def reverse_transaction(transaction, user, notes):
    '''
    We will create a duplicate transaction, but switch the 
    debit and credit accounts.

    We only reverse posted items
    '''
    if transaction is None:
        raise Exception("Please provide a valid transaction")

    if user is None or not user.pk:
        raise Exception("Please provide a valid user")

    if notes is None:
        raise Exception("Please provide a valid note")

    transaction_type = transaction.transaction_type
    POSTED = 1

    if transaction.last_status_id == POSTED:
        with db_transaction.atomic():
            #get all the transaction entries
            entries = transaction.entries.all()

            assert entries.count() == 2

            #get the entries
            debit_entry  = entries.get(item_type=LedgerTransactionEntry.DEBIT)
            credit_entry = entries.get(item_type=LedgerTransactionEntry.CREDIT)

            #get the accounts from the entries
            credit_account = credit_entry.ledger_account
            debit_account = debit_entry.ledger_account

            #get the other particulars
            product_account = transaction.product_account
            amount = transaction.amount
            currency = transaction.currency
                
            #status is set to none, as it will be received as pending
            status = None

            return create_transaction(
                transaction_type=transaction_type,  
                credit_account=debit_account, #switch items around
                debit_account=credit_account, #switch items around
                product_account=product_account,
                reversing_transaction=transaction,
                amount=amount,
                status=status,
                user=user, 
                notes=notes,
            )

def update_transaction_status(transaction, status_code, user, notes):
    if transaction is None:
        raise Exception("Please provide a valid transaction")

    if status_code is None:
        raise Exception("Please provide a valid status code")

    if user is None or not user.pk:
        raise Exception("Please provide a valid user")

    if notes is None:
        raise Exception("Please provide a valid note")

    with db_transaction.atomic():
        #get the transaction status and time now
        config_transaction_status = ConfigLedgerTransactionStatus.objects.get(code=status_code)
        status_date = timezone.now()

        #create the transaction status
        transaction_status = LedgerTransactionStatus.objects.create(
            transaction=transaction,
            transaction_status=config_transaction_status,
            transaction_status_date=status_date,
            notes=notes,
            created_by=user,
        )
        #update the transaction with the new status and date
        transaction.last_status = transaction_status
        transaction.last_status_date = status_date
        transaction.save()

    return transaction_status
