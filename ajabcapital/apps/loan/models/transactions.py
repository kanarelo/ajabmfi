from __future__ import unicode_literals

from django.db import models

from decimal import Decimal as D

from ajabcapital.apps.core.models import AuditBase, ConfigBase

class LoanLedgerAccount(AuditBase):
    name = models.CharField(max_length=100)
    
    gl_code = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = "loan_ledger_account"
        verbose_name = "Loan Ledger Account"

    def __str__(self):
        return "(%s) %s" % (self.gl_code, self.name)

class LoanRepaymentAllocationOrder(AuditBase):
    product = models.ForeignKey('LoanProduct')

    allocation_item = models.ForeignKey('ConfigRepaymentAllocationItem')
    rank = models.PositiveIntegerField()

    class Meta:
        db_table = "loan_repayment_allocation_order"
        verbose_name = "Loan Repayment Allocation Order"

    def __str__(self):
        return "(%s) %s" % (self.code, self.name)

class LoanProductAccountingRule(AuditBase):
    product = models.ForeignKey('LoanProduct', related_name="accounting_rules")
    transaction_type = models.ForeignKey('ConfigLoanTransactionType', related_name="accounting_rules")

    debit_account  = models.ForeignKey('LoanLedgerAccount', related_name="debits")
    credit_account = models.ForeignKey('LoanLedgerAccount', related_name="credits")

    class Meta:
        db_table = "loan_accounting_rule"
        verbose_name = "Loan Accounting Rule"

class LoanProductFundSource(AuditBase):
    name = models.CharField(max_length=100)

    product = models.ForeignKey('LoanProduct', related_name="fund_sources")
    base_account  = models.ForeignKey('LoanLedgerAccount')

    class Meta:
        db_table = "loan_fund_source"
        verbose_name = "Loan Fund Source"

    def __str__(self):
        return "(%s) %s" % (self.product, self.base_account)

    @property
    def ll_code(self):
        return "%s.%s0%s" % (
            self.base_account.gl_code, 
            self.product.pk, 
            self.pk if (self.pk > 9) else ("0%s" % self.pk)
        )

class LoanProductControlAccount(AuditBase):
    name = models.CharField(max_length=100)

    product = models.OneToOneField('LoanProduct', related_name="control_account")
    base_account  = models.ForeignKey('LoanLedgerAccount')

    rules = models.CharField(max_length=1000)

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

class LoanTransaction(AuditBase):
    transaction_type = models.ForeignKey("ConfigLoanTransactionType")
    status = models.ForeignKey("ConfigLoanAccountTransactionStatus", related_name="transactions")

    amount   = models.DecimalField(max_digits=18, decimal_places=4, default=D('0.0'))
    notified = models.BooleanField(default=False)

    class Meta:
        db_table = "loan_transaction"
        verbose_name = "Loan Account Transaction"

class LoanAccountTransactionEntry(AuditBase):
    '''
    We separate all the loan product transactions from the GL transactions
    '''
    CREDIT = 0
    DEBIT  = 1
    ITEM_TYPES = (
        (CREDIT, 'Credit'),
        (DEBIT, 'Debit'),
    )

    ACCOUNTS_LEDGER = 1
    LOAN_LEDGER = 2
    LEDGER_TYPES = (
        (ACCOUNTS_LEDGER, "Loan accounts ledger entry"),
        (LOAN_LEDGER, "Loan ledger entry"),
    )

    transaction = models.ForeignKey('LoanTransaction', related_name="entries")
    
    item_type = models.IntegerField(choices=ITEM_TYPES)

    #involved accounts
    loan_ledger_account = models.ForeignKey('LoanLedgerAccount', related_name="transactions", null=True)
    loan_account = models.ForeignKey('LoanAccount', related_name="transactions", null=True)

    ledger_type = models.IntegerField(choices=LEDGER_TYPES)

    ledger_balance_increment = models.DecimalField(
        decimal_places=4, max_digits=18, default=D('0.0')
    )

    class Meta:
        db_table = "loan_account_transaction_entry"
        verbose_name = "Loan Account Transaction Entry"
        verbose_name_plural = "Loan Account Transaction Entries"
