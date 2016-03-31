from __future__ import unicode_literals

from django.contrib.postgres.fields import JSONField
from django.db import models

from decimal import Decimal as D

from ajabcapital.apps.core.models import (
    AuditBase, 
    ConfigBase, 
    BaseTransactionBlock, 
    BaseTransactionBlockItem
)

class LoanRepaymentAllocationOrder(AuditBase):
    allocation_item = models.ForeignKey('ConfigRepaymentAllocationItem')
    rank = models.PositiveIntegerField()

    class Meta:
        db_table = "loan_repayment_allocation_order"
        verbose_name = "Loan Repayment Allocation Order"

    def __str__(self):
        return "(%s) %s" % (self.product.name, self.allocation_item.name)

class LoanChartOfAccounts(AuditBase):
    loan_portfolio_control_account = models.ForeignKey('core.LedgerAccount', related_name="loan_portfolio")
    loan_funding_source_account = models.ForeignKey('core.LedgerAccount', related_name="loan_funding")
    loan_interest_income_receivable_account = models.ForeignKey('core.LedgerAccount', related_name="loan_interest_receivable")
    loan_interest_income_account = models.ForeignKey('core.LedgerAccount', related_name="loan_interest_income")
    loan_fee_income_receivable_account = models.ForeignKey('core.LedgerAccount', related_name="loan_fee_receivable")
    loan_fee_income_account = models.ForeignKey('core.LedgerAccount', related_name="loan_fee_income")
    loan_penalty_income_receivable_account = models.ForeignKey('core.LedgerAccount', related_name="loan_penalty_receivable")
    loan_penalty_income_account = models.ForeignKey('core.LedgerAccount', related_name="loan_penalty_income")
    loan_principal_write_off_expense_account = models.ForeignKey('core.LedgerAccount', related_name="loan_principal_writeoff")
    loan_interest_write_off_expense_account = models.ForeignKey('core.LedgerAccount', related_name="loan_interest_writeoff")
    loan_penalty_write_off_expense_account = models.ForeignKey('core.LedgerAccount', related_name="loan_penalty_writeoff")
    loan_fee_write_off_expense_account = models.ForeignKey('core.LedgerAccount', related_name="loan_fee_writeoff")

    class Meta:
        db_table = "loan_chart_of_accounts"

#---------------------------------------------------
class LoanProductBlock(BaseTransactionBlock):
    '''
    This ledger is for high level, accounts, those that are defined by the system.
    Blocks record and confirm when and in what sequence 
    transactions enter and are logged in the block chain.
    '''
    class Meta:
        db_table = "loan_product_transaction_block"
        verbose_name = "Loan Product Block"

class LoanProductBlockItem(BaseTransactionBlockItem):
    '''
    '''
    block = models.ForeignKey('LoanProductBlock', related_name="block_items")

    class Meta:
        db_table = "loan_product_transaction_block_item"
        verbose_name = "Loan Product Block Item"

#---------------------------------------------------------------
class LoanAccountBlock(BaseTransactionBlock):
    '''
    This ledger is for credit profile transactions, 
    Basically accruals, repayments and disbursments.
    '''
    class Meta:
        db_table = "loan_account_transaction_block"
        verbose_name = "Loan Account Block"

class LoanAccountBlockItem(BaseTransactionBlockItem):
    '''
    '''
    ledger_account = models.ForeignKey('LoanAccount')
    block = models.ForeignKey('LoanAccountBlock', related_name="block_items")

    class Meta:
        db_table = "loan_account_transaction_block_item"
        verbose_name = "Loan Account Block Item"
