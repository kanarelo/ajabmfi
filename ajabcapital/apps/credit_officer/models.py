from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from ajabcapital.apps.core.models import AuditBase, ConfigBase

class CreditOfficerProfile(AuditBase):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        db_table = "credit_office_profile"
        verbose_name = "Credit Officer Profile"

class CreditOfficerPortfolio(AuditBase):
    credit_officer = models.ForeignKey('CreditOfficerProfile')
    account = models.ForeignKey('loan.LoanAccount')

    class Meta:
        db_table = "credit_office_portfolio"
        verbose_name = "Credit Officer Portfolio"