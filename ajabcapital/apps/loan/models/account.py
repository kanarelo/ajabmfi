from __future__ import unicode_literals

from django.conf import settings

from django.db import models

from decimal import Decimal as D

from ajabcapital.apps.core.models import AuditBase, ConfigBase

class LoanProfile(AuditBase):
    user  = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name="loan_accounts", 
        related_query_name="loan_account"
    )

    #counters
    no_of_loans = models.PositiveIntegerField()
    no_of_current_loans = models.PositiveIntegerField()
    no_of_closed_loans = models.PositiveIntegerField()

    #timestamps
    first_disbursal = models.DateTimeField()
    last_repayment = models.DateTimeField()

    credit_limit = models.DecimalField(
        decimal_places=2, max_digits=18, default=D('0.0')
    )

    class Meta:
        db_table = "loan_profile"
        verbose_name = "Loan Profile"

class LoanGroup(AuditBase):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = "loan_group"
        verbose_name = "Loan Group"

class LoanProfileGroup(AuditBase):
    loan_profile = models.ForeignKey('LoanProfile')
    loan_group = models.ForeignKey('LoanGroup')

    class Meta:
        db_table = "loan_profile_group"
        verbose_name = "Loan Profile Group"

class LoanAccount(AuditBase):
    '''
    These are the Client Loan Accounts.
    '''
    product = models.ForeignKey('LoanProduct', 
        related_name="product_accounts", related_query_name="product_account")

    loan_profile_group = models.ForeignKey('LoanProfileGroup', null=True)
    loan_profile = models.ForeignKey('LoanProfile', null=True)

    risk_classification = models.ForeignKey('ConfigLoanRiskClassification')

    account_number = models.CharField(unique=True, db_index=True, max_length=20)

    amortization_type = models.ForeignKey('ConfigAmortizationType', blank=True, null=True)
    currency = models.ForeignKey('core.ConfigCurrency', blank=True, null=True)

    repayment_period_unit = models.ForeignKey("ConfigLoanPeriodUnit", related_name="repayments")
    repayment_period = models.IntegerField()
    repayment_installments = models.IntegerField()

    grace_period_unit = models.ForeignKey("ConfigLoanPeriodUnit", related_name="grace_periods")
    grace_period = models.IntegerField(default=0)

    notes = models.CharField(max_length=800, null=True, blank=True)
    
    #Interest rate per period unit
    interest_rate = models.DecimalField(max_digits=6, decimal_places=4, default=D('0.0'))

    last_current_balance = models.DecimalField(max_digits=18, decimal_places=4, default=D('0.0'))
    last_current_balance_date = models.DateTimeField()

    last_overdue_balance = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True)
    last_overdue_balance_date = models.DateTimeField()
    
    last_repayment_amount = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True)
    last_repayment_date = models.DateTimeField()
    
    last_disbursal_amount = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True)
    last_disbursal_date = models.DateTimeField()

    def __str__(self):
        return "#%s: %s for %s" % (self.account_number, self.product, self.holder)

    class Meta:
        db_table = "loan_account"
        verbose_name = "Loan Account"

class LoanAccountStatus(AuditBase):
    account = models.ForeignKey('LoanAccount', related_name="statuses")

    status = models.ForeignKey('ConfigLoanAccountStatus', related_name="statuses")
    reason = models.CharField(max_length=140, null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, 
        related_name='approvals_on_loan_accounts', null=True, blank=True)

    class Meta:
        db_table = "loan_account_status"
        verbose_name = "Loan Account Status"
        verbose_name_plural = "Loan Account Statuses"
