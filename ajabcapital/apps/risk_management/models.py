from __future__ import unicode_literals

from django.conf import settings

from django.db import models

from decimal import Decimal as D

from ajabcapital.apps.core.models import AuditBase, ConfigBase

class ConfigLoanRiskClassification(ConfigBase):
    color = models.CharField(max_length=15, null=True)
    default_provision = models.DecimalField(decimal_places=4, max_digits=7, default=D(0.0))
    icon = models.FileField(upload_to="config/icons/", null=True, blank=True)

    class Meta:
        db_table = "config_loan_risk_classification"
        verbose_name = "Config Loan Risk Classification"

class RiskProfile(AuditBase):
    loan_profile = models.OneToOneField('loan.LoanProfile', related_name="risk_profile")

    is_performing = models.BooleanField()
    is_guarantor = models.BooleanField(default=False)
    has_fraud = models.BooleanField(default=False)
    has_current_delinquency = models.BooleanField()
    has_historical_delinquency = models.BooleanField()

    total_no_of_applications = models.PositiveIntegerField()
    current_risk_classification = models.ForeignKey(
        'ConfigLoanRiskClassification', 
        related_name="classified_loans", 
        related_query_name="classified_loan", 
        null=True, blank=True
    )
    current_risk_classification_date = models.DateTimeField(null=True, blank=True)

    min_days_in_arrears = models.PositiveIntegerField()
    max_days_in_arrears = models.PositiveIntegerField()

    total_current_credit_exposure = models.DecimalField(
        max_digits=18, decimal_places=4, null=True, blank=True)

    class Meta:
        db_table = "risk_profile"
        verbose_name = "Risk Profile"

class ProfileRiskClassification(AuditBase):
    profile = models.ForeignKey('RiskProfile', related_name="risk_classifications")

    classification = models.ForeignKey('ConfigLoanRiskClassification', related_name="classifications")
    reason = models.CharField(max_length=140, null=True, blank=True)

    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, 
        related_name='approvals_on_loan_risk_status', null=True, blank=True)

    class Meta:
        db_table = "risk_profile_risk_status"
        verbose_name = "Risk Profile Risk Classification"

    def __unicode__(self):
        return "%s, %s" % (self.account, self.classification)
