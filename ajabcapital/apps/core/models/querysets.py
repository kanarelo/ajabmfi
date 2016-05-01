from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from decimal import Decimal as D

ASSET = "1"
LIABILITY = "2"
EQUITY = "3"
INCOME = "4"
EXPENSE = "5"

GENERAL_LEDGER = "LGT_001"
LOAN_LEDGER = "LGT_002"

NORMAL_DIRECTION = "LBD_001"
CONTRA_DIRECTION = "LBD_002"

LEVEL_1 = "LVL_001"
LEVEL_2 = "LVL_002"

PENDING_POSTING = 'LTS_001'
POSTED = 'LTS_002'
WITHELD = 'LTS_003'
SETTLED = 'LTS_004'

LOAN_DISBURSAL = "TT_001"
LOAN_REPAYMENT = "TT_014"
INTEREST_ACCRUAL = "TT_002"
FEE_ACRUAL = "TT_003"
PENALTY_ACCRUAL = "TT_004"
PRINCIPAL_POSTING = "TT_005"
INTEREST_POSTING = "TT_006"
FEE_POSTING = "TT_007"
PENALTY_POSTING = "TT_008"
PRINCIPAL_WRITE_OFF= "TT_009"
INTEREST_WRITE_OFF = "TT_010"
FEE_WRITE_OFF = "TT_011"
PENALTY_WRITE_OFF = "TT_012"
BAD_LOAN_RECOVERY = "TT_013"

class LedgerAccountQueryset(models.QuerySet):
    #---account category------------
    def asset(self):
        return self.filter(account_category__code=ASSET)

    def liability(self):
        return self.filter(account_category__code=LIABILITY)

    def equity(self):
        return self.filter(account_category__code=EQUITY)

    def income(self):
        return self.filter(account_category__code=INCOME)

    def expense(self):
        return self.filter(account_category__code=EXPENSE)

    #---ledger type ----------------
    def general_ledger_accounts(self):
        return self.filter(ledger_type__code=GENERAL_LEDGER)

    def loan_ledger_accounts(self):
        return self.filter(ledger_type__code=LOAN_LEDGER)

    #---balance direction-----------
    def contra(self):
        return self.filter(balance_direction__code=CONTRA_DIRECTION)

    def normal(self):
        return self.filter(balance_direction__code=NORMAL_DIRECTION)

class LedgerTransactionQueryset(models.QuerySet):
    #--------------------------------
    def reversed_transactions(self):
        return self.filter(reversing_transaction__isnull=True)

    #--------product accounts--------
    def product_transactions(self):
        return self.filter(
            product_type__isnull=False,
            product_account__isnull=False,
        )

    def loan_transactions(self):
        return self.product_transactions().filter(
            product_type=self.model.LOAN
        )

    def loan_account_transactions(self, account_number):
        return self.loan_transactions().filter(
            product_account=account_number
        )

    #---------notification-----------
    def notified(self):
        return self.filter(notified=True)

    def unnotified(self):
        return self.filter(notified__isnull=True)

    def notification_failed(self):
        return self.filter(notified=False)

    #----------status----------------
    def pending_postings(self):
        return self.filter(last_status__code=PENDING_POSTING)

    def posted(self):
        return self.filter(last_status__code=POSTED)

    def witheld(self):
        return self.filter(last_status__code=WITHELD)

    def settled(self):
        return self.filter(last_status__code=SETTLED)

    #----------transaction types-----
    def loan_disbursal(self):
        return self.filter(transaction_type__code=LOAN_DISBURSAL)

    def loan_repayments(self):
        return self.filter(transaction_type__code=LOAN_REPAYMENT)

    #---------
    def interest_accruals(self):
        return self.filter(transaction_type__code=INTEREST_ACCRUAL)

    def fee_accruals(self):
        return self.filter(transaction_type__code=FEE_ACRUAL)

    def penalty_accruals(self):
        return self.filter(transaction_type__code=PENALTY_ACCRUAL)

    #---------
    def principal_postings(self):
        return self.filter(transaction_type__code=PRINCIPAL_POSTING)

    def interest_postings(self):
        return self.filter(transaction_type__code=INTEREST_POSTING)

    def fee_postings(self):
        return self.filter(transaction_type__code=FEE_POSTING)

    def penalty_postings(self):
        return self.filter(transaction_type__code=PENALTY_POSTING)

    #---------
    def principal_write_offs(self):
        return self.filter(transaction_type__code=PRINCIPAL_WRITE_OFF)

    def interest_write_offs(self):
        return self.filter(transaction_type__code=INTEREST_WRITE_OFF)

    def fee_write_offs(self):
        return self.filter(transaction_type__code=FEE_WRITE_OFF)

    def penalty_write_offs(self):
        return self.filter(transaction_type__code=PENALTY_WRITE_OFF)

    #---------
    def bad_loan_recovery(self):
        return self.filter(transaction_type__code=BAD_LOAN_RECOVERY)


class LedgerEntryQueryset(models.QuerySet):
    #----------status----------------
    def pending_postings(self):
        return self.filter(ledger_transaction__last_status__code=PENDING_POSTING)

    def posted(self):
        return self.filter(ledger_transaction__last_status__code=POSTED)

    def witheld(self):
        return self.filter(ledger_transaction__last_status__code=WITHELD)

    def settled(self):
        return self.filter(ledger_transaction__last_status__code=SETTLED)

    #----------item types--------
    def credits(self, *args, **kwargs):
        return self.filter(ledger_balance_item_type=self.model.CREDIT, *args, **kwargs)

    def debits(self, *args, **kwargs):
        return self.filter(ledger_balance_item_type=self.model.DEBIT, *args, **kwargs)

    #--------transactions--------
    def transaction_items(self, transaction=None, transaction_no=None):
        return self.filter(
            Q(ledger_transaction=transaction)|
            Q(ledger_transaction__transaction_no=transaction_no)
        )

    #--------product account entries
    def product_account_entries(self):
        return self.filter(
            product_account__isnull=False
        )

    def product_account_transaction_entries(self, product_account):
        return self.product_account_entries().filter(
            product_account=product_account
        )

    def product_accounts_transaction_entries(self, product_accounts):
        return self.product_account_entries().filter(product_account__in=product_accounts)

    def account_entries(self, ledger_account=None, ledger_code=None):
        return self.filter(
            Q(ledger_account=ledger_account) |
            Q(ledger_account__ledger_code=ledger_code)
        )

    #--------transaction_types
    def loan_disbursal(self):
        return self.filter(ledger_transaction__transaction_type__code=LOAN_DISBURSAL)

    def loan_repayment(self):
        return self.filter(ledger_transaction__transaction_type__code=LOAN_REPAYMENT)

    #---------
    def interest_accruals(self):
        return self.filter(ledger_transaction__transaction_type__code=INTEREST_ACCRUAL)

    def fee_accruals(self):
        return self.filter(ledger_transaction__transaction_type__code=FEE_ACRUAL)

    def penalty_accruals(self):
        return self.filter(ledger_transaction__transaction_type__code=PENALTY_ACCRUAL)

    #---------
    def principal_postings(self):
        return self.filter(ledger_transaction__transaction_type__code=PRINCIPAL_POSTING)

    def interest_postings(self):
        return self.filter(ledger_transaction__transaction_type__code=INTEREST_POSTING)

    def fee_postings(self):
        return self.filter(ledger_transaction__transaction_type__code=FEE_POSTING)

    def penalty_postings(self):
        return self.filter(ledger_transaction__transaction_type__code=PENALTY_POSTING)

    #---------
    def principal_write_offs(self):
        return self.filter(ledger_transaction__transaction_type__code=PRINCIPAL_WRITE_OFF)

    def interest_write_offs(self):
        return self.filter(ledger_transaction__transaction_type__code=INTEREST_WRITE_OFF)

    def fee_write_offs(self):
        return self.filter(ledger_transaction__transaction_type__code=FEE_WRITE_OFF)

    def penalty_write_offs(self):
        return self.filter(ledger_transaction__transaction_type__code=PENALTY_WRITE_OFF)

    #---------
    def bad_loan_recovery(self):
        return self.filter(ledger_transaction__transaction_type__code=BAD_LOAN_RECOVERY)
