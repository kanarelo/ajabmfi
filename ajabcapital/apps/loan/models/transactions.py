from __future__ import unicode_literals

from django.contrib.postgres.fields import JSONField
from django.db import models

from decimal import Decimal as D

from ajabcapital.apps.core.models import AuditBase, ConfigBase

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

class LoanProductFundSource(AuditBase):
    name = models.CharField(max_length=100)
    product = models.ForeignKey('LoanProduct', related_name="fund_sources")

    class Meta:
        db_table = "loan_fund_source"
        verbose_name = "Loan Fund Source"

    def __str__(self):
        return "(%s) %s" % (self.product, self.base_account)

class LoanTransactionRegister(AuditBase):
    transaction  = models.ForeignKey('core.LedgerTransaction', related_name="loan_register")

    class Meta:
        db_table = "loan_transaction_register"
        verbose_name = "Loan Transaction Register"
