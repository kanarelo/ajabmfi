from __future__ import unicode_literals

from django.db import models

from decimal import Decimal as D

from ajabcapital.apps.core.models import AuditBase, ConfigBase

from .querysets import *

class ConfigFeeCalculationMethod(ConfigBase):
    class Meta:
        db_table = "config_fee_calculation_method"
        verbose_name = "Config Fee Calculation Method"

class ConfigGracePeriodType(ConfigBase):
    class Meta:
        db_table = "config_grace_period_type"
        verbose_name = "Config Grace Period Type"

class ConfigInterestCalculationMethod(ConfigBase):
    icon = models.FileField(upload_to="config/icons/", null=True, blank=True)

    class Meta:
        db_table = "config_interest_calculation_method"
        verbose_name = "Config Interest Calculation Method"

class ConfigLoanAccountStatus(ConfigBase):
    icon = models.FileField(upload_to="config/icons/", null=True, blank=True)

    class Meta:
        db_table = "config_loan_account_status"
        verbose_name = "Config Loan Account Status"
        verbose_name_plural = "Config Loan Account Statuses"

class ConfigRepaymentFrequency(ConfigBase):
    class Meta:
        db_table = "config_repayment_frequency"
        verbose_name = "Config Repayment Frequency"
        verbose_name_plural = "Config Repayment Frequencies"

class ConfigRepaymentAllocationItem(ConfigBase):
    class Meta:
        db_table = "config_repayment_allocation_item"
        verbose_name = "Config Repayment Allocation Item"

class ConfigLoanPeriodUnit(ConfigBase):
    frequencies = models.ManyToManyField('ConfigRepaymentFrequency')

    class Meta:
        db_table = "config_loan_period_unit"
        verbose_name = "Config Loan Period Unit"

class ConfigLoanProductChannel(ConfigBase):
    icon = models.FileField(upload_to="config/icons/channels/", null=True, blank=True)

    class Meta:
        db_table = "config_loan_product_channel"
        verbose_name = "Config Loan Product Channel"

class ConfigLoanFundType(ConfigBase):
    icon = models.FileField(upload_to="config/icons/channels/", null=True, blank=True)

    class Meta:
        db_table = "config_loan_fund_type"
        verbose_name = "Config Loan Fund Type"

class ConfigLoanProductType(ConfigBase):
    icon = models.FileField(upload_to="config/icons/", null=True, blank=True)

    class Meta:
        db_table = "config_loan_product_type"
        verbose_name = "Config Loan Product Type"

class ConfigLoanProductFeeType(ConfigBase):
    class Meta:
        db_table = "config_loan_product_fee_type"
        verbose_name = "Config Loan Product Fee Type"

class ConfigProfileType(ConfigBase):
    icon = models.FileField(upload_to="config/icons/profile_types/", null=True, blank=True)    

    class Meta:
        db_table = "config_profile_type"
        verbose_name = "Config Profile Type"

class ConfigRepaymentModel(ConfigBase):
    class Meta:
        db_table = "config_repayment_model"
        verbose_name = "Config Repayment Model"
