from __future__ import unicode_literals

from django.conf import settings

from django.db import models

from decimal import Decimal as D

from ajabcapital.apps.core.models import AuditBase, ConfigBase

class RiskProfile(AuditBase):
    loan_profile = models.OneToOneField('loan.LoanProfile', related_name="risk_profile")

    is_performing = models.BooleanField()
    is_guarantor = models.BooleanField(default=False)
    has_fraud = models.BooleanField(default=False)
    has_current_delinquency = models.BooleanField()
    has_historical_delinquency = models.BooleanField()

    total_no_of_applications = models.PositiveIntegerField()
    worst_risk_classification = models.ForeignKey('loan.ConfigLoanRiskClassification')

    min_days_in_arrears = models.PositiveIntegerField()
    max_days_in_arrears = models.PositiveIntegerField()

    total_current_credit_exposure = models.DecimalField(
        max_digits=18, decimal_places=4, null=True, blank=True)

    class Meta:
        db_table = "risk_profile"
        verbose_name = "Risk Profile"
