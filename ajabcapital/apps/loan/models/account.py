from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from decimal import Decimal as D

from ajabcapital.apps.core.models import (
    AuditBase
)

from .querysets import LoanAccountQuerySet, LoanProfileQueryset

class LoanProfile(AuditBase):
    credit_limit = models.DecimalField(decimal_places=2, max_digits=18, null=True)

    individual_profile = models.ForeignKey('crm.IndividualProfile', 
        null=True, related_name="individual_loan_profiles",
        related_query_name="individual_loan_profile"
    )
    business_profile = models.ForeignKey('crm.BusinessProfile', 
        null=True, related_name="business_loan_profiles",
        related_query_name="business_loan_profile"
    )
    group_profile = models.ForeignKey('crm.GroupProfile', 
        null=True, related_name="group_loan_profiles",
        related_query_name="group_loan_profile"
    )

    profile_type = models.ForeignKey('ConfigProfileType')

    objects = LoanProfileQueryset.as_manager()

    class Meta:
        db_table = "loan_profile"
        verbose_name = "Loan Profile"

    def __unicode__(self):
        return "%s" % (self.profile() or "N/P")

    def profile(self):
        return (
            self.individual_profile or 
            self.business_profile or 
            self.group_profile
        )

class LoanAccount(AuditBase):
    '''
    These are the client loan accounts
    '''
    NORMAL_RISK_CLASSIFICATION = 6

    loan_profile = models.ForeignKey('LoanProfile', 
        related_name="loan_accounts", related_query_name="loan_account"
    )

    account_number = models.CharField(unique=True, db_index=True, max_length=20)
    product = models.ForeignKey('LoanProduct', 
        related_query_name="product_account", related_name="product_accounts"
    )
    notes = models.CharField(max_length=800, null=True, blank=True)

    current_risk_classification = models.ForeignKey(
        'risk_management.ConfigLoanRiskClassification', 
        related_query_name='classified_loan_account',
        related_name='classified_loan_accounts',
        null=True, blank=True
    )
    current_risk_classification_date = models.DateTimeField(null=True, blank=True)

    #LOOKUP_FIELDS
    #time stamps
    current_account_status = models.ForeignKey('ConfigLoanAccountStatus')
    current_account_status_date = models.DateTimeField(null=True)
    date_disbursed  = models.DateTimeField(null=True)
    
    #account balance
    current_balance = models.DecimalField(max_digits=18, decimal_places=4, default=D('0.0'))
    current_balance_date = models.DateTimeField(null=True)

    #repayments stamps
    last_installment_date = models.DateTimeField(null=True)
    next_installment_date = models.DateTimeField(null=True)
    last_installment_amount = models.DecimalField(max_digits=18, decimal_places=4, default=D('0.0'))
    next_installment_amount = models.DecimalField(max_digits=18, decimal_places=4, default=D('0.0'))

    #overdues stamps
    principal_due  = models.DecimalField(max_digits=18, decimal_places=4, default=D('0.0'))
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
            self.principal_due + 
            self.interest_accrued + 
            self.fees_accrued +
            self.penalties_accrued
        )

    class Meta:
        db_table = "loan_account"
        verbose_name = "Loan Account"

class LoanTerm(AuditBase):
    loan_account = models.ForeignKey('LoanAccount', related_name="terms", related_query_name="term")

    loan_amount = models.DecimalField(max_digits=18, decimal_places=4, default=D('0.0'))
    loan_amount_currency = models.ForeignKey('core.ConfigCurrency', blank=True, null=True)
    
    terms_restructured = models.ForeignKey('LoanTerm', null=True, blank=True)
    terms_restructured_date = models.DateTimeField(null=True, blank=True)

    repayment_period = models.PositiveIntegerField()
    repayment_period_unit = models.ForeignKey("ConfigLoanPeriodUnit", related_name="repayments")
    repayment_frequency = models.ForeignKey("ConfigRepaymentFrequency", db_column='payment_frequency')

    grace_period = models.IntegerField(null=True)
    grace_period_unit = models.ForeignKey("ConfigLoanPeriodUnit", related_name="grace_periods", null=True)

    interest_rate = models.DecimalField(max_digits=6, decimal_places=4, default=D('0.0'))
    interest_rate_unit = models.ForeignKey("ConfigLoanPeriodUnit", related_name="interest_rates", default=5)

    class Meta:
        db_table = "loan_term"
        verbose_name = "Loan Term"

    def __unicode__(self):
        return self.loan_account.account_number

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
        return "%s, %s" % (self.account, self.status)

