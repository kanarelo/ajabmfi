from django.db.models import Q, Sum, F

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.db import transaction as db_transaction, IntegrityError

from ..utils import get_reference_no, record_log

import logging
from decimal import Decimal as D

from ..models import *
from ...loan.facades import *

INITIAL = D('0.0')

PENDING_POSTING = "pending_posting"
POSTED = "posted"

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
    ASSET = "A"
    LIABILITY = "L"
    EQUITY = "E"
    INCOME = "I"
    EXPENSE = "E"

    if (amount is None) or (not amount):
        raise Exception("Invalid amount")

    if account.account_category.code in (ASSET, EXPENSE):
        #Assets and expenses increase with debit
        if (item_type == LedgerEntry.DEBIT):
            amount = +(amount)
        #Yet they decrease with credits
        elif (item_type == LedgerEntry.CREDIT):
            amount = -(amount)

    elif account.account_category.code in (LIABILITY, EQUITY, INCOME):
        #Liability, Equity and Income accounts decrease with debits
        if (item_type == LedgerEntry.DEBIT): 
            amount = -(amount)
        #Yet they increase with credits
        elif (item_type == LedgerEntry.CREDIT):
            amount = +(amount)

    else:
        raise Exception("Invalid account category")

    #constants
    NORMAL_ACCOUNT = "N"
    CONTRA_ACCOUNT = "C"

    account_type_code = account.balance_direction.code

    #normal account
    if account_type_code == NORMAL_ACCOUNT:
        #for normal accounts, return amount as it is by this point
        return +(amount)
    elif account_type_code == CONTRA_ACCOUNT:
        #a contra account is a general ledger account which is intended 
        #to have its balance be the opposite of the normal balance for 
        #that account classification
        #In that case, lets negate the balance, so that we can get its opposite
        return -(amount)

def create_transaction(
    transaction_type=None, credit_account=None, debit_account=None, 
    currency=None, product_account=None, amount=None, status=None, 
    user=None, notes=None, reversing_transaction=None, transaction_no=None,
    transaction_date=None, *args, **kwargs
):
    if not transaction_no:
        transaction_no = get_reference_no()

    if transaction_date is None:
        transaction_date = timezone.now()

    if status is None:
        transaction_status = ConfigLedgerTransactionStatus.objects.get(code=PENDING_POSTING)
    else:
        transaction_status = status

    def create_transaction_obj():
        #check if the transaction number exists in the db
        if not LedgerTransaction.objects.filter(
            transaction_no=transaction_no
        ).exists():
            #create the transaction
            transaction = LedgerTransaction(
                transaction_type=transaction_type,
                last_status=transaction_status,
                last_status_date=transaction_date,
                transaction_no=transaction_no,
                reversing_transaction=reversing_transaction,
                currency=currency,
                amount=amount,
                notes=notes,
                created_by=user
            )

            #set the product account
            if product_account is not None:
                transaction.product_account = product_account.account_number

            #save transaction
            transaction.save()

            status = LedgerTransactionStatus.objects.create(
                transaction=transaction,
                transaction_status=transaction_status,
                transaction_status_date=transaction_date,
                notes="Transaction status by %s " % user,
                created_by=user
            )

            l = dict(
                transaction_type=transaction_type.code,
                last_status=transaction_status,
                last_status_date=transaction_date,
                reversing_transaction=reversing_transaction,
                transaction_no=transaction_no,
                amount=amount,
                currency=currency,
                user=user,
                **kwargs
            )

            if (credit_account and debit_account):
                l.update(
                    credit_account=credit_account.ledger_code,
                    debit_account=debit_account.ledger_code,
                )

            if (product_account is not None):
                l.update(product_account=product_account.account_number)

            record_log(**l)
            return transaction
        else:
            return create_transaction_obj()

    def create_transaction_entry(transaction, ledger_account, item_type, increment):
        #Adds entry for transaction
        return LedgerEntry.objects.create(
            ledger_balance_item_type=item_type,
            ledger_balance_increment=increment,
            ledger_transaction=transaction,
            product_account=transaction.product_account,
            ledger_account=ledger_account,
            created_by=user,
        )

    with db_transaction.atomic():
        if not (
            (amount and currency) and 
            (user) and
            (transaction_type and notes)
        ):
            raise Exception("Please provide valid parameters for this transaction.")

        transaction = create_transaction_obj()
        (debit_entry, credit_entry) = (None, None)

        if (debit_account and credit_account):
            #get the debit and credit ledger balance increments to use for the entries
            debit_ledger_balance_increment  = get_ledger_balance_increment(
                amount, debit_account, LedgerEntry.DEBIT
            )
            credit_ledger_balance_increment = get_ledger_balance_increment(
                amount, credit_account, LedgerEntry.CREDIT
            )

            if (debit_ledger_balance_increment and credit_ledger_balance_increment):
                #Adds credit entry for transaction
                debit_entry  = create_transaction_entry(
                    transaction, 
                    debit_account,  
                    LedgerEntry.DEBIT, 
                    debit_ledger_balance_increment
                )
                credit_entry = create_transaction_entry(
                    transaction, 
                    credit_account, 
                    LedgerEntry.CREDIT, 
                    credit_ledger_balance_increment
                )
                return (debit_entry, credit_entry)
            else:
                raise Exception("Increments not found")
        else:
            return transaction


def reverse_transaction(transaction, user, notes, transaction_date=None):
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
    
    if transaction.last_status.code == (POSTED,):
        with db_transaction.atomic():
            #get all the transaction entries
            entries = transaction.entries.all()

            assert entries.count() == 2

            #get the entries
            debit_entry  = entries.get(item_type=LedgerEntry.DEBIT)
            credit_entry = entries.get(item_type=LedgerEntry.CREDIT)

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
                credit_account=debit_account,
                debit_account=credit_account,
                product_account=product_account,
                reversing_transaction=transaction,
                transaction_date=transaction_date,
                amount=amount,
                status=status,
                user=user, 
                notes=notes,
            )

def update_transaction_status(transaction, status_code, user, notes, status_date=None):
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

        if not status_date:
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
        transaction.last_status = config_transaction_status
        transaction.last_status_date = status_date
        transaction.save()

    return transaction_status
