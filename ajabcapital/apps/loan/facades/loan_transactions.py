import uuid
import random
import math
import names
import radar

from calendar import monthrange
from datetime import timedelta, datetime
from dateutil import relativedelta
from decimal  import Decimal as D

from django.db.models import Q, Sum, F

from django.utils import timezone
from django.db import transaction as db_transaction

from ..utils import *
from ...core.utils import *
from ...core.facades import *
from .loan_account import *

import logging

logger = logging.getLogger(__name__)

INITIAL = D('0.0')

GENDERS = ['female', 'male']

FEE = "AI_001"
PENALTY = "AI_002"
INTEREST = "AI_003"
PRINCIPAL = "AI_004"

FEE_PERCENTAGE = "FC_001"
FEE_FLAT = "FC_002"

PERFORMING = "AS_006"
DISBURSEMENT = "AS_007"

FLAT = "CM_001"

PENDING_POSTING = "LTS_001"
POSTED = "LTS_002"

TRANSACTION_TYPE_DEFERRED_LIABILITY = "TT_015"
TRANSACTION_TYPE_LOAN_REPAYMENT = "TT_014"
TRANSACTION_TYPE_LOAN_DISBURSAL = "TT_001"
TRANSACTION_TYPE_FEE_POSTING = "TT_007"
TRANSACTION_TYPE_PENALTY_POSTING = "TT_008"
TRANSACTION_TYPE_PRINCIPAL_POSTING = "TT_005"
TRANSACTION_TYPE_INTEREST_POSTING = "TT_006"

def create_loan_transaction(
    loan_account, amount, user, 
    transaction_type, status=None, 
    notes=None, currency=None, 
    transaction_date=None,
    *args, **kwargs
):  
    with db_transaction.atomic():

        if transaction_type.posts_to_ledger:
            debit_account, credit_account = get_transaction_type_account_turple(transaction_type)
        else:
            debit_account, credit_account = (None, None)
            logger.info("Transaction does not support ledger posting")

        if status is None:
            status = ConfigLedgerTransactionStatus.objects.get(code=PENDING_POSTING)

        txn = create_transaction(
            transaction_type=transaction_type,
            transaction_date=transaction_date,
            credit_account=credit_account,
            debit_account=debit_account,
            product_account=loan_account,
            amount=amount,
            status=status,
            user=user, 
            notes=notes,
            currency=currency,
            *args, **kwargs
        )

        if type(txn) == tuple:
            (debit_entry, credit_entry) = txn
        else:
            return txn

        return (debit_entry, credit_entry)

def allocate_repayment(loan_account, amount, user, *args, **kwargs):
    #get the loan product from the account
    loan_product = loan_account.product
    loan_term = loan_account.terms.latest('created_at')
    transaction_date = timezone.now()

    def create_allocation_transaction(
        allocation_order_item, 
        accrued_item, 
        allocation_dictionary, 
        allocated_count, 
        allocation_balance
    ):
        #put aside the variables from the turple
        transaction_type = allocation_dictionary['transaction_type']
        accrued_amount   = allocation_dictionary['amount']

        #if allocation item is equal to accrued item code, and accrued amount is more than 1
        #Check to ensure we do not get to negative numbers
        if (
            (allocation_order_item == accrued_item) and 
            (accrued_amount > 0) and 
            (allocation_balance > 0)
        ):
            #if amount accrued is sizable, deduct
            (debit_entry, credit_entry) = create_loan_transaction(
                loan_account, 
                accrued_amount, 
                user,
                currency=loan_term.loan_amount_currency,
                transaction_type=transaction_type, 
                transaction_date=transaction_date,
                # notes="automatic repayment allocation..."
            )

            #stamp new allocation
            allocated_count += 1

            #deduct amount posted from balance
            allocation_balance -= accrued_amount

        return (allocated_count, allocation_balance)

    def apply_allocations(amount, total_accruals, allocation_order_items):
        #Ensure we have sane values
        if amount > D('0.0'):
            #setup allocation balance, to help us check to total allocation
            allocated_count    = 0
            allocation_balance = amount

            #Loop through the allocation order
            for allocation_order_item in allocation_order_items:
                #Loop through all the accruals we are expecting to collect
                for accrued_item, allocation_dictionary in accruals.iteritems():
                    if allocation_balance > D('0.0'):
                        (allocated_count, allocation_balance) = create_allocation_transaction(
                            allocation_order_item, 
                            accrued_item, 
                            allocation_dictionary, 
                            allocated_count, 
                            allocation_balance
                        )
                    else:
                        MESSAGE = "Error, amount not allowed"
                        logger.debug(MESSAGE)
                        send_notification_to_profile(loan_account.loan_profile, MESSAGE)

            current_balance = get_loan_account_current_balance(loan_account)

            loan_account.last_repayment_date = timezone.now()
            loan_account.last_current_balance = current_balance

            loan_account.save()
        else:
            logger.debug("amount: %s and total_accruals %s" % (amount, total_accruals))
            raise Exception("Amount Not Sufficient")

    #This is a private API, just for allocation purposes
    def get_accruals_mapping(allocation_order_items):
        #fetch the transaction types
        transaction_types = ConfigLedgerTransactionType.objects.filter(
            is_active=True, 
            code__in=[
                TRANSACTION_TYPE_FEE_POSTING,
                TRANSACTION_TYPE_PENALTY_POSTING,
                TRANSACTION_TYPE_INTEREST_POSTING,
                TRANSACTION_TYPE_PRINCIPAL_POSTING
            ]
        )

        #set the accruals ready for mapping
        accruals = dict()

        #Loop through the allocation_order_items
        for allocation_order_item in allocation_order_items:
            allocation_item = allocation_order_item.allocation_item

            amount = None

            for transaction_type in transaction_types:
                #at the end of the panel
                
                #get the value for the account: it's a turple, the amount to be used and the function
                if (allocation_item.code == FEE) and (transaction_type.code == TRANSACTION_TYPE_FEE_POSTING):
                    amount = get_fees_due_on_loan_account(loan_account)
                elif (allocation_item.code == PENALTY) and (transaction_type.code == TRANSACTION_TYPE_PENALTY_POSTING):
                    amount = get_penalties_due_on_loan_account(loan_account)
                elif (allocation_item.code == INTEREST) and (transaction_type.code == TRANSACTION_TYPE_INTEREST_POSTING):
                    amount = get_interest_due_on_loan_account(loan_account)
                elif (allocation_item.code == PRINCIPAL) and (transaction_type.code == TRANSACTION_TYPE_PRINCIPAL_POSTING):
                    amount = get_principal_due_on_loan_account(loan_account)

                if (amount is not None):
                    #get the key of the dictionary
                    key = allocation_order_item.allocation_item
                    #get the value, a tuple of transaction type, and amount
                    value = {
                        'amount': amount, 
                        'transaction_type': transaction_type
                    }
                    #update the accruals dictionary
                    accruals.update({ key : value })
                    break

        return accruals

    with db_transaction.atomic():
        #get the current balance owed by the client (principal balance)
        current_balance = get_loan_account_current_balance(loan_account)

        #get the allocation order items
        allocation_order_items = LoanRepaymentAllocationOrder.objects.all().order_by('rank')
        #get the accruals on the account
        accruals = get_accruals_mapping(allocation_order_items)

        total_accruals = sum(i['amount'] for i in accruals.values())
        loan_balance = (total_accruals + current_balance)

        if (amount > loan_balance) and (loan_balance > 0):
            deferred_balance = (amount - loan_balance)

            transaction_type = ConfigLedgerTransactionType.objects.get(
                code=TRANSACTION_TYPE_DEFERRED_LIABILITY
            )

            (debit_entry, credit_entry) = create_loan_transaction(
                loan_account, 
                deferred_balance, 
                user,
                currency=loan_term.loan_amount_currency,
                transaction_type=transaction_type, 
                transaction_date=transaction_date,
                notes="Deferred payment: [Overpayment for Loan %s]" % loan_account.account_number,
                *args, **kwargs
            )

            logger.warning("Deferred Balance: %s, %d" % (loan_account.account_number, deferred_balance))

        apply_allocations(amount, total_accruals, allocation_order_items)

def disburse_loan(
    loan_account, 
    user, 
    status=None, 
    transaction_date=None, 
    notes=None, 
    *args, **kwargs
):
    with db_transaction.atomic():
        loan_term = loan_account.terms.latest('created_at')
        loan_product = loan_account.product

        if not transaction_date:
            transaction_date = timezone.now()

        transaction_type = ConfigLedgerTransactionType.objects.get(code=TRANSACTION_TYPE_LOAN_DISBURSAL)
        account_status = ConfigLoanAccountStatus.objects.get(code=DISBURSEMENT)

        (debit_entry, credit_entry) = create_loan_transaction(
            loan_account, 
            loan_term.loan_amount, 
            user,
            currency=loan_term.loan_amount_currency,
            transaction_type=transaction_type, 
            transaction_date=transaction_date,
            status=status,
            notes=notes,
        )

        transaction_type = ConfigLedgerTransactionType.objects.get(code=TRANSACTION_TYPE_FEE_POSTING)
        fees = loan_product.fees.filter(charged_at=LoanProductFee.DISBURSEMENT)
        total_fee = D('0.0')

        for fee in fees:
            if fee.fee_calculation.code == FEE_PERCENTAGE:
                amount = loan_term.loan_amount * (fee.amount / D('100.0'))
            elif fee.fee_calculation.code == FEE_FLAT:
                amount = fee.amount
            else:
                break

            (debit_entry, credit_entry) = create_loan_transaction(
                loan_account, 
                amount, 
                user,
                currency=loan_term.loan_amount_currency,
                transaction_type=transaction_type,
                transaction_date=transaction_date,
                status=status,
                notes=notes
            )

            total_fee += amount

        loan_account.current_account_status = account_status
        loan_account.current_account_status_date = transaction_date

        loan_account.date_disbursed = transaction_date
        loan_account.current_balance_date = transaction_date
        disbursal_amount = (loan_term.loan_amount - total_fee)
        loan_account.current_balance = disbursal_amount

        loan_account.save()

        return (debit_entry, credit_entry)

def add_loan_repayment(
    loan_account, 
    amount, 
    user, 
    status=None,
    transaction_date=None, 
    notes=None, 
    *args, **kwargs
):
    transaction_type = ConfigLedgerTransactionType.objects.get(
        code=TRANSACTION_TYPE_LOAN_REPAYMENT
    )
    loan_term = loan_account.terms.latest('created_at')

    if notes is None:
        notes = "loan repayment by %s" % user

    if transaction_date is None:
        transaction_date = timezone.now()

    with db_transaction.atomic():
        txn = create_loan_transaction(
            loan_account, 
            amount, 
            user,
            transaction_type=transaction_type, 
            transaction_date=transaction_date,
            currency=loan_term.loan_amount_currency,
            status=status,
            notes=notes,
            *args, **kwargs
        )
        logger.debug("Repayment #%s queued for Loan Account %s" % (
                txn.transaction_no, txn.product_account
            )
        )
        return txn

