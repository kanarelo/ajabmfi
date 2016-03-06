from decimal import Decimal as D

from django.db.models import Q, Sum, F

from django.utils import timezone
from django.db import transaction as db_transaction

from ajabcapital.core.utils import *
from ajabcapital.core.facades import *

from ..utils import *

import logging

INITIAL = D('0.0')

def create_loan_transaction(
    loan_account, amount, user, transaction_type, *args, **kwargs
):
    with db_transaction.atomic():
        try:
            #get the accounting rules for this product's transaction type
            debit_account, credit_account = get_transaction_type_account_turple(transaction_type)
        except LoanProductAccountingRule.DoesNotExist:
            raise Exception("Please set the Loan Product Rules for the product %s" % )

        (debit_entry, credit_entry) = create_transaction(
            transaction_type=transaction_type,
            credit_account=credit_account,
            debit_account=debit_account,
            product_account=loan_account.account_number,
            amount=amount,
            status=status,
            user=user, 
            *args, **kwargs
        )

        return (debit_entry, credit_entry)

def allocate_repayment(loan_account, amount, *args, **kwargs):
    logger = logging.getLogger(__name__)
    #get the loan product from the account
    loan_product = loan_account.product

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
            create_loan_transaction(
                loan_account, accrued_amount, 
                transaction_type=transaction_type
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
                        logger.debug("Seems you have repaid less than expected!")
                        send_notification_to_profile(
                            loan_account.loan_profile,
                            "Seems you have repaid less than expected!"
                        )

            loan_account.last_repayment_date = timezone.now()
            loan_account.last_current_balance = get_loan_account_balance(loan_account)

            loan_account.save()
        else:
            logger.debug("amount: %s and total_accruals %s" % (amount, total_accruals))
            raise Exception("Amount Not Sufficient")

    #This is a private API, just for allocation purposes
    def get_accruals_mapping(allocation_order_items):
        #fetch the transaction types
        transaction_types = ConfigLoanTransactionType.objects.filter(is_active=True)

        TRANSACTION_TYPE_FEE_POSTING = "TT_007"
        TRANSACTION_TYPE_PENALTY_POSTING = "TT_008"
        TRANSACTION_TYPE_PRINCIPAL_POSTING = "TT_005"
        TRANSACTION_TYPE_INTEREST_POSTING = "TT_006"

        FEE = "AI_001"
        PENALTY = "AI_002"
        INTEREST = "AI_003"
        PRINCIPAL = "AI_004"

        #set the accruals ready for mapping
        accruals = {}

        #Loop through the allocation_order_items
        for allocation_order_item in allocation_order_items:
            allocation_item = allocation_order_item.allocation_item
            if allocation_item.code == FEE:
                #get the value for the account: it's a turple, the amount to be used and the function
                transaction_type = transaction_types.get(code=TRANSACTION_TYPE_FEE_POSTING)
                amount = get_fees_due_on_loan_account(loan_account)
            elif allocation_item.code == PENALTY:
                transaction_type = transaction_types.get(code=TRANSACTION_TYPE_PENALTY_POSTING)
                amount = get_penalties_due_on_loan_account(loan_account)
            elif allocation_item.code == INTEREST:
                transaction_type = transaction_types.get(code=TRANSACTION_TYPE_INTEREST_POSTING)
                amount = get_interest_due_on_loan_account(loan_account)
            elif allocation_item.code == PRINCIPAL:
                transaction_type = transaction_types.get(code=TRANSACTION_TYPE_PRINCIPAL_POSTING)
                amount = get_principal_due_on_loan_account(loan_account)

            #get the key of the dictionary
            key = allocation_order_item.allocation_item
            #get the value, a tuple of transaction type, and amount
            value = {'amount': amount, 'transaction_type': transaction_type}
            #update the accruals dictionary
            accruals.update({ key : value })

        return accruals

    with db_transaction.atomic():
        #get the current balance owed by the client (principal balance)
        current_balance = loan_account.last_current_balance
        #get the overdue balance: (principal + fees + penalties + interest)
        overdue_balance = loan_account.last_overdue_balance

        #get the allocation order items
        allocation_order_items = LoanRepaymentAllocationOrder.objects.filter(
            product=loan_product
        ).order_by('rank')
        #get the accruals on the account
        accruals = get_accruals_mapping(allocation_order_items)

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

        #finally apply the accruals if the total accruals sound sane
        if total_accruals > D('0.0'):
            apply_allocations(amount, total_accruals, allocation_order_items)

def apply_accruals(loan_account, user):
    '''
    accruals are done everyday at 4am-6am
    '''
    def next_accrual_date():
        repayment_frequency = loan_account.repayment_frequency
        next_date_on_frequency = next_date_on_frequency

    def last_accrual_date():
        repayment_frequency = loan_account.repayment_frequency
        next_date_on_frequency = next_date_on_frequency

    def has_accrual_matured(time_past_since_disbursement):
        IRREGULAR_SCHEDULE = "RF_009"
        REVOLVING = "RF_010"
        BULLET = "RF_011"

        DAYS_IN_A_MONTH = 30.4375

        DAILY = ("RF_001", 1) #Repayment Period > (365 / (1)) 
        WEEKLY = ("RF_002", 7) #Repayment Period > (365 / (7 * 1))
        FORTNIGHTLY = ("RF_003", 14) #Repayment Period > (365 / (7 * 2))
        MONTHLY = ("RF_004", DAYS_IN_A_MONTH) #Repayment Period > (365 / 12)
        EVERY_TWO_MONTHS = ("RF_005", (2 * DAYS_IN_A_MONTH)) #Repayment Period > (365 / 6)
        THRICE_A_YEAR = ("RF_007", (4 * DAYS_IN_A_MONTH)) #Repayment Period > (365 / 4)
        QUARTERLY = ("RF_008", (3 * DAYS_IN_A_MONTH)) #Repayment Period > 365 (365 / 3)
        TWICE_A_YEAR = ("RF_006", (6 * DAYS_IN_A_MONTH)) #Repayment Period > (365 / 2)
        ANNUALLY = ("RF_012", (12 * DAYS_IN_A_MONTH)) #Repayment Period > 365 (365 / 1)

        last_accrual_date = loan_account.last_accrual_date

        if loan_account.repayment_frequency.code in (
            IRREGULAR_SCHEDULE, REVOLVING, BULLET
        ):
            return False
        elif loan_account.repayment_frequency.code == DAILY[0]:
            return True

    date_today = timezone.now()
    date_disbursed = loan_account.last_disbursal_date

    if date_disbursed is None:
        raise Exception(
            "You cannot apply accruals on Un-disbursed Loan %s" % 
            loan_account.account_number
        )

    with db_transaction.atomic():
        #a tuple (days, hours, minutes, seconds)
        time_past_since_disbursement = get_time_diff(date_disbursed, date_today)

        #get the grace period in days
        grace_period_time_turple = time_units_to_turple(
            loan_account.grace_period, 
            loan_account.grace_period_unit
        )
        repayment_period_time_turple = time_units_to_turple(
            loan_account.repayment_period, 
            loan_account.repayment_period_unit   
        )

        #Check if we are within the repayment period
        within_repayment_period = (time_past_since_disbursement < repayment_period_time_turple)

        accrual_has_matured = within_repayment_period
        accrual_has_matured &= has_accrual_matured(time_past_since_disbursement)

        if accrual_has_matured:
            principal_due = D('0.0')
            interest_due  = D('0.0')

            #Check if we are within the grace period
            within_grace_period = (time_past_since_disbursement < grace_period_time_turple)
            
            FULL_GRACE_PERIOD = "GPT_001"
            PRINCIPAL_GRACE_PERIOD = "GPT_002"

            if within_grace_period:
                if (loan_account.product.grace_period_type.code == FULL_GRACE_PERIOD):
                    return #Dont do nothing :D
                elif (loan_account.product.grace_period_type.code == PRINCIPAL_GRACE_PERIOD):
                    interest_due = get_interest_due(loan_account, grace_period_type=PRINCIPAL_GRACE_PERIOD)
            else:
                principal_due, interest_due = get_repayment_due_on_loan_account(loan_account)

            #=================
            TRANSACTION_TYPE_PRINCIPAL_POSTING = "TT_005"
            TRANSACTION_TYPE_INTEREST_POSTING = "TT_006"

            transaction_types = ConfigLoanTransactionType.objects.filter(is_active=True)
            tt_principal_posting = transaction_types.get(TRANSACTION_TYPE_PRINCIPAL_POSTING)
            tt_interest_posting  = transaction_types.get(TRANSACTION_TYPE_INTEREST_POSTING)
            
            INTEREST = "AI_003"
            PRINCIPAL = "AI_004"
                
            if interest_due > 0:
                transaction_type = 
                create_loan_transaction(
                    loan_account, interest_due, user, transaction_type=tt_interest_posting
                )

def disburse_loan(loan_account, *args, **kwargs):
    with db_transaction.atomic():
        validation_facades.validate_disbursement(loan_account)

        (debit_entry, credit_entry) = create_loan_transaction(
            loan_account, 
            loan_account.amount, 
            transaction_type=codes.TRANSACTION_TYPE_LOAN_DISBURSAL, 
            *args, **kwargs
        )

        loan_account.status = LoanAccount.ACTIVE
        loan_account.date_disbursed = timezone.now()

        loan_account.save()

        return (debit_entry, credit_entry)
