from __future__ import unicode_literals

from django.db import models

from decimal import Decimal as D

from ajabcapital.apps.core.models import *

class ConfigAmortizationType(ConfigBase):
    class Meta:
        db_table = "config_amortization_type"
        verbose_name = "Config Amortization Type"

class ConfigCurrency(ConfigBase):
    class Meta:
        db_table = "config_currency"
        verbose_name = "Config Currency"
        verbose_name_plural = "Config Currencies"

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

class ConfigRepaymentAllocationItem(ConfigBase):
    class Meta:
        db_table = "config_repayment_allocation_item"

class ConfigLoanAccountTransactionStatus(ConfigBase):
    icon = models.FileField(upload_to="config/icons/", null=True, blank=True)

    class Meta:
        db_table = "config_loan_account_transaction_status"
        verbose_name = "Config Loan Transaction Status"
        verbose_name_plural = "Config Loan Transaction Statuses"

class ConfigLoanPeriodUnit(ConfigBase):
    class Meta:
        db_table = "config_loan_period_unit"
        verbose_name = "Config Loan Period Unit"

class ConfigLoanProductType(ConfigBase):
    icon = models.FileField(upload_to="config/icons/", null=True, blank=True)

    class Meta:
        db_table = "config_loan_product_type"
        verbose_name = "Config Loan Product Type"

class ConfigLoanProductFeeType(ConfigBase):
    class Meta:
        db_table = "config_loan_product_fee_type"
        verbose_name = "Config Loan Product Fee Type"

class ConfigLoanPipelineStep(ConfigBase):
    class Meta:
        db_table = "config_loan_pipeline_step"
        verbose_name = "Config Loan Pipeline Step"    
        
class ConfigLoanTransactionType(ConfigBase):
    icon = models.FileField(upload_to="config/icons/", null=True, blank=True)

    class Meta:
        db_table = "config_loan_transaction_type"
        verbose_name = "Config Loan Transaction Type"
    
class ConfigPaymentFrequency(ConfigBase):
    class Meta:
        db_table = "config_payment_frequency"
        verbose_name = "Config Payment Frequency"
        verbose_name_plural = "Config Payment Frequencies"
    
class ConfigLoanRiskClassification(ConfigBase):
    icon = models.FileField(upload_to="config/icons/", null=True, blank=True)

    class Meta:
        db_table = "config_loan_risk_classification"
        verbose_name = "Config Loan Risk Classification"
