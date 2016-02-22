from __future__ import unicode_literals

from django.contrib.postgres.fields import JSONField
from django.db import models

from decimal import Decimal as D

from ajabcapital.apps.core.models import AuditBase, ConfigBase

class LoanProductAccountingRule(AuditBase):
    transaction_type = models.ForeignKey(
        'core.ConfigLedgerTransactionType', related_name="accounting_rules"
    )
    product = models.ForeignKey('LoanProduct', related_name="accounting_rules")

    debit_account  = models.ForeignKey('core.LedgerAccount', related_name="debits")
    credit_account = models.ForeignKey('core.LedgerAccount', related_name="credits")

    class Meta:
        db_table = "loan_accounting_rule"
        verbose_name = "Loan Accounting Rule"

class LoanProductFundSource(AuditBase):
    name = models.CharField(max_length=100)
    product = models.ForeignKey('LoanProduct', related_name="fund_sources")

    base_account = models.ForeignKey('core.LedgerAccount')

    class Meta:
        db_table = "loan_fund_source"
        verbose_name = "Loan Fund Source"

    def __str__(self):
        return "(%s) %s" % (self.product, self.base_account)

class LoanProductControlAccount(AuditBase):
    name = models.CharField(max_length=100)

    product = models.OneToOneField('LoanProduct')
    base_account  = models.ForeignKey('core.LedgerAccount')

    meta = JSONField(default="{}")

    class Meta:
        db_table = "loan_product_control_account"
        verbose_name = "Loan Product Control"

    def __str__(self):
        return "(%s) %s" % (self.product, self.base_account)

    @property
    def ll_code(self):
        return "%s.%s0%s" % (
            self.base_account.gl_code, 
            self.product.pk, 
            self.pk if (self.pk > 9) else ("0%s" % self.pk)
        )

class LoanTransactionRegister(AuditBase):
    transaction  = models.ForeignKey('core.LedgerTransaction', related_name="loan_register")

    loan_account = models.ForeignKey('LoanAccount')

    class Meta:
        db_table = "loan_transaction_register"
        verbose_name = "Loan Transaction Register"
