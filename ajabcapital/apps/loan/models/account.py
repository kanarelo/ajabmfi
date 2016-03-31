from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from decimal import Decimal as D

from ajabcapital.apps.core.models import (
    AuditBase
)

from .querysets import LoanAccountQuerySet

class LoanProfile(AuditBase):
    credit_limit = models.DecimalField(decimal_places=2, max_digits=18, null=True)

    individual_profile = models.ForeignKey('crm.IndividualProfile', null=True)
    business_profile = models.ForeignKey('crm.BusinessProfile', null=True)
    group_profile = models.ForeignKey('crm.GroupProfile', null=True)

    profile_type = models.ForeignKey('ConfigProfileType')

    class Meta:
        db_table = "loan_profile"
        verbose_name = "Loan Profile"

    def __unicode__(self):
        return "%s" % (
            self.individual_profile or 
            self.business_profile or 
            self.group_profile or 
            "N/P"
        )

class LoanAccount(AuditBase):
    '''
    These are the client loan accounts
    '''
    NORMAL_RISK_CLASSIFICATION = 6

    loan_profile = models.ForeignKey('LoanProfile')

    account_number = models.CharField(unique=True, db_index=True, max_length=20)
    product = models.ForeignKey('LoanProduct', 
        related_query_name="product_account",
        related_name="product_accounts"
    )
    risk_classification = models.ForeignKey('ConfigLoanRiskClassification', default=NORMAL_RISK_CLASSIFICATION)
    repayment_model = models.ForeignKey('ConfigRepaymentModel')
    
    notes = models.CharField(max_length=800, null=True, blank=True)

    #LOOKUP_FIELDS
    #time stamps
    current_account_status = models.ForeignKey('ConfigLoanAccountStatus')
    current_account_status_date = models.DateTimeField(null=True)
    
    #account balance
    current_balance = models.DecimalField(max_digits=18, decimal_places=4, default=D('0.0'))
    current_balance_date = models.DateTimeField(null=True)

    #repayments stamps
    last_repayment_date    = models.DateTimeField(null=True)
    next_repayment_date    = models.DateTimeField(null=True)
    last_repayment_amount  = models.DecimalField(max_digits=18, decimal_places=4, default=D('0.0'))
    next_repayment_amount  = models.DecimalField(max_digits=18, decimal_places=4, default=D('0.0'))

    #overdues stamps
    principal_overdue  = models.DecimalField(max_digits=18, decimal_places=4, default=D('0.0'))
    interest_accrued   = models.DecimalField(max_digits=18, decimal_places=4, default=D('0.0'))
    fees_accrued       = models.DecimalField(max_digits=18, decimal_places=4, default=D('0.0'))
    penalties_accrued  = models.DecimalField(max_digits=18, decimal_places=4, default=D('0.0'))
    last_accruals_date = models.DateTimeField(null=True)
    next_accruals_date = models.DateTimeField(null=True)

    objects = LoanAccountQuerySet.as_manager()

    def __unicode__(self):
        return "#%s: %s for %s" % (self.account_number, self.product, self.loan_profile)

    @property
    def total_overdues(self):
        return (
            self.principal_overdue + 
            self.interest_accrued + 
            self.fees_accrued
        )

    class Meta:
        db_table = "loan_account"
        verbose_name = "Loan Account"

class LoanTerm(AuditBase):
    loan_account = models.ForeignKey('LoanAccount', related_name="terms", related_query_name="term")

    loan_amount = models.DecimalField(max_digits=18, decimal_places=4, default=D('0.0'))
    loan_amount_currency = models.ForeignKey('core.ConfigCurrency', blank=True, null=True)
    loan_amount_disbursal_date = models.DateTimeField(null=True)

    terms_restructured = models.ForeignKey('LoanTerm', null=True)
    terms_restructured_date = models.DateTimeField(null=True)

    repayment_period = models.PositiveIntegerField()
    repayment_period_unit = models.ForeignKey("ConfigLoanPeriodUnit", related_name="repayments")
    repayment_frequency = models.ForeignKey("ConfigRepaymentFrequency", db_column='payment_frequency')

    grace_period = models.IntegerField(null=True)
    grace_period_unit = models.ForeignKey("ConfigLoanPeriodUnit", related_name="grace_periods", null=True)

    #Interest rate per period unit
    interest_rate = models.DecimalField(max_digits=6, decimal_places=4, default=D('0.0'))

    class Meta:
        db_table = "loan_term"
        verbose_name = "Loan Term"

    def __unicode__(self):
        return (
            self.loan_account.account_number
        )

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

    def __unicode__(self):
        return "%s, %s" % (
            self.account,
            self.status 
        )

class LoanRiskClassification(AuditBase):
    account = models.ForeignKey('LoanAccount', related_name="risk_classifications")

    classification = models.ForeignKey('ConfigLoanRiskClassification', related_name="classifications")
    reason = models.CharField(max_length=140, null=True, blank=True)

    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, 
        related_name='approvals_on_loan_risk_status', null=True, blank=True)

    class Meta:
        db_table = "loan_risk_status"
        verbose_name = "Loan Risk Classification"
        verbose_name_plural = "Loan Risk Classification"

    def __unicode__(self):
        return "%s, %s" % (
            self.account,
            self.classification 
        )
