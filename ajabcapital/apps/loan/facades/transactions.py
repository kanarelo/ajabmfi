from decimal import Decimal as D

from django.db.models import Q, Sum, F

from django.utils import timezone
from django.db import transaction as db_transaction

from ajabcapital.core.utils import (
    get_reference_no
)

import logging

INITIAL = D('0.0')

def get_sum_of_account_transaction_items(entries):
    return entries.aggregate(ledger_balance=Sum('ledger_balance_increment')).pop(
        'ledger_balance'
    ) or INITIAL

def get_transaction_account_turple(product, transaction_type):
    accounting_rule = LoanProductAccountingRule.objects.get(
        product=product, 
        transaction_type=transaction_type
    )
    return (debit_account, credit_account)

def create_loan_transaction(
    loan_account, amount, approved_by=None, status=codes.POSTED,
    transaction_type=None, transaction_id=None, 
    destination_account=None, *args, **kwargs
):
    with db_transaction.atomic():
        try:
            debit_account, credit_account = get_transaction_account_turple(
                loan_account.product, transaction_type
            )
        except LoanProductAccountingRule.DoesNotExist:
            return (None, None)

        posting_date = timezone.now()

        transaction = LoanTransaction.objects.create(
            transaction_type=transaction_type,
            status=status,
            amount=amount
        )

        debit_entry = LedgerTransaction.objects.create(
            ledger_balance_increment=get_ledger_balance_increment(
                amount, 
                debit_account, 
                codes.DEBIT
            ),
            status=status,
            created_by=approved_by,
            transaction=transaction,
            item_type=codes.DEBIT,
            loan_ledger_account=debit_account,
            loan_account=loan_account,
            amount=amount,
            transaction_type=transaction_type,
            posting_date=posting_date
        )
        credit_entry = LedgerTransaction.objects.create(
            ledger_balance_increment=get_ledger_balance_increment(
                amount, 
                credit_account, 
                codes.CREDIT
            ),
            created_by=approved_by,
            transaction=transaction,
            status=status,
            item_type=codes.CREDIT,
            account=-(destination_account or loan_account),
            gl_account_code=credit_account,
            amount=amount,
            transaction_type=transaction_type,
            posting_date=posting_date
        )

        record_log(
            account=loan_account,
            loan_profile=loan_account.loan_profile,
            credit_gl_account_code=credit_account.ll_code,
            debit_gl_account_code=debit_account.ll_code,
            transaction_type=transaction_type,
            transaction_id=transaction_id,
            approved_by=approved_by,
            status=status,
            amount=amount,
            **kwargs
        )
        return (debit_entry, credit_entry)

def get_accruals_mapping(loan_account):
    accruals = {}
    loan_product = loan_account.product

    transaction_types = ConfigLoanTransactionType.objects.all()

    for allocation_order_item in allocation_order_items:
        allocation_item = allocation_order_item.allocation_item
        if allocation_item.code == "AI_001":#Fee
            #get the value for the account: it's a turple, the amount to be used and the function
            transaction_type = transaction_types.get(code="TT_008")
            amount = fees_due_on_loan_account(loan_account)
        elif allocation_item.code == "AI_002":#Penalty
            transaction_type = transaction_types.get(code="TT_007")
            amount = penalties_due_on_loan_account(loan_account)
        elif allocation_item.code == "AI_003":#interest
            transaction_type = transaction_types.get(code="TT_006")
            amount = interest_due_on_loan_account(loan_account)
        elif allocation_item.code == "AI_004":#Principal
            transaction_type = transaction_types.get(code="TT_005")
            amount = principal_due_on_loan_account(loan_account)

        #get the key of the dictionary
        key = allocation_order_item.allocation_item
        #get the value, a tuple of transaction type, and amount
        value = (amount, transaction_type)

        #update the accruals dictionary
        accruals.update({ key : value })

    return accruals

def allocate_repayment(loan_account, amount, *args, **kwargs):
    logger = logging.getLogger(__name__)
    #get the loan product from the account
    loan_product = loan_account.product

    with db_transaction.atomic():
        #get the current balance owed by the client (principal balance)
        current_balance = loan_account.last_current_balance
        #get the overdue balance: (principal + fees + penalties + interest)
        overdue_balance = loan_account.last_overdue_balance

        total_accruals = sum(i[0] for i in accruals.values())

        #Ensure that our data is corrent, the accruals need to be equal to the overdue balance
        assert (overdue_balance == total_accruals)

        deferred_balance = D('0.0')
        loan_balance = (total_accruals + current_balance)

        if amount > loan_balance:
            deferred_balance = (amount - loan_balance)
            #set the new amount as the (current_balance + total_accruals)
            amount = loan_balance

            #TODO: Do something with the deferred balance
            logger.warning("Deferred Balance: %d" % deferred_balance)

        if total_accruals > D('0.0'):
            #get the allocation order items
            allocation_order_items = LoanRepaymentAllocationOrder.objects.filter(
                product=loan_product
            ).order_by('rank')
            #get the accruals on the account
            accruals = get_accruals_mapping(loan_account, allocation_order_items)

            #Ensure we have sane values
            if amount > D('0.0'):
                transaction_no = get_reference_no(15)

                #setup allocation balance, to help us check to total allocation
                allocation_balance = amount

                #if total accruals is greater than zero
                if total_accruals > D('0.0'):
                    allocated_count = 0
                    #Loop through the allocation order
                    for allocation_order_item in allocation_order_items:
                        #Loop through all the accruals we are expecting to collect
                        for accrued_item, allocation_tuple in accruals.iteritems():
                            #put aside the variables from the turple
                            accrued_amount, transaction_type = allocation_tuple

                            #if allocation item is equal to accrued item code, and accrued amount is more than 1
                            #Check to ensure we do not get to negative numbers
                            if (
                                (allocation_order_item == accrued_item) and 
                                (accrued_amount > 0) and 
                                (allocation_balance > 0)
                            ):
                                #if amount accrued is sizable, deduct
                                create_transaction(
                                    loan_account, accrued_amount, 
                                    transaction_no=transaction_no,
                                    transaction_type=transaction_type
                                )

                                #stamp new allocation
                                allocated_count += 1

                                #deduct amount posted from balance
                                allocation_balance -= accrued_amount

                if allocation_balance > D('0.0'):
                    (loan_account, allocation_balance, transaction_no=transaction_no)

                loan_account.last_repayment_date = timezone.now()
                loan_account.last_current_balance = 

                loan_account.save()
            else:
                logger.debug("amount: %s and total_accruals %s" % (amount, total_accruals))
                raise Exception("Amount Not Sufficient")

def apply_accruals(loan_account, approved_by=None):
    with db_transaction.atomic():
        date_disbursed = loan_account.date_disbursed

        if date_disbursed is None:
            raise Exception(
                "You cannot apply accruals on Un-disbursed Loan %s" % loan_account.account_number)

        date_today = timezone.now()
        month_diff = month_delta(date_disbursed, date_today, days_of_the_month=30)
        
        if loan_account.grace_period:
            grace_period = loan_account.grace_period
            grace_period_type = loan_account.loan_product.grace_period_type

            within_grace_period = (
                (month_diff - grace_period) < 1
            )
            within_repayment_period = (
                (month_diff - loan_account.repayment_period) < 1
            )

            #No need to proceed, we don't want to accrue anything 
            interest_due = 0

            if (not grace_period == 0): 
                if (within_grace_period):
                    if (grace_period_type == LoanProduct.FULL_GRACE_PERIOD):
                        pass
                    elif (grace_period_type == LoanProduct.PRINCIPAL_GRACE_PERIOD):
                        principal_due = loan_account.amount
                        interest_due = (
                            (principal_due * loan_account.interest_rate) /
                            loan_account.repayment_period
                        )
            else:
                if within_repayment_period:
                    principal_due = loan_account_principal_due(loan_account)
                    interest_due = (
                        (principal_due * (loan_account.interest_rate / D('100.0'))) /
                        loan_account.repayment_period
                    )
                
            if interest_due > 0:
                apply_interest_to_account(loan_account, interest_due)

def disburse_loan(loan_account, *args, **kwargs):
    with db_transaction.atomic():
        validation_facades.validate_disbursement(loan_account)

        debit_entry, credit_entry = create_transaction(
            loan_account, loan_account.amount, 
            transaction_type=codes.TRANSACTION_TYPE_LOAN_DISBURSAL, *args, **kwargs
        )

        loan_account.status = LoanAccount.ACTIVE
        loan_account.date_disbursed = timezone.now()

        loan_account.save()

        return (debit_entry, credit_entry)

def apply_interest_to_account(loan_account, amount, *args, **kwargs):
    return create_transaction(loan_account, amount, 
        transaction_type=codes.TRANSACTION_TYPE_INTEREST_APPLY, *args, **kwargs)

def apply_fee_to_account(loan_account, amount, *args, **kwargs):
    return create_transaction(loan_account, amount, 
        transaction_type=codes.TRANSACTION_TYPE_FEE_APPLY, *args, **kwargs)

def apply_penalty_to_account(loan_account, amount, *args, **kwargs):
    return create_transaction(loan_account, amount, 
        transaction_type=codes.TRANSACTION_TYPE_PENALTY_APPLY, *args, **kwargs)
