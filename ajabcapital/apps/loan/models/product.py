from __future__ import unicode_literals

from django.db import models

from decimal import Decimal as D

from ajabcapital.apps.core.models import AuditBase, ConfigBase

from .querysets import LoanProductQueryset

class LoanFund(AuditBase):
    name = models.CharField(max_length=100)

    fund_type = models.ForeignKey('ConfigLoanFundType')
    profile_type = models.ForeignKey('ConfigProfileType')
    product_type = models.ForeignKey('ConfigLoanProductType')
    repayment_model = models.ForeignKey('ConfigRepaymentModel')
    product_channel = models.ForeignKey('ConfigLoanProductChannel', null=True)
    
    fund_credit_limit = models.DecimalField(decimal_places=2, max_digits=18, null=True)
    loan_credit_limit = models.DecimalField(decimal_places=2, max_digits=18, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "loan_fund"
        verbose_name = "Loan Fund"

class LoanProduct(AuditBase):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=140)
    is_active = models.BooleanField(default=False)

    color = models.CharField(max_length=15, null=True)

    loan_fund = models.ForeignKey('LoanFund')
    product_channel = models.ForeignKey('ConfigLoanProductChannel')
    repayment_model = models.ForeignKey('ConfigRepaymentModel')

    product_type = models.ForeignKey('ConfigLoanProductType')

    default_repayment_frequency = models.ForeignKey(
        "ConfigRepaymentFrequency", db_column='payment_frequency', default=1)
    default_repayment_period = models.IntegerField(default=0)
    default_repayment_period_unit = models.ForeignKey(
        "ConfigLoanPeriodUnit", related_name="repayment_products")
    
    repayment_grace_period_type = models.ForeignKey("ConfigGracePeriodType", 
        null=True, blank=True, db_column="grace_period_type")
    default_repayment_grace_period = models.IntegerField(
        null=True, blank=True, db_column="default_grace_period")
    default_repayment_grace_period_unit = models.ForeignKey("ConfigLoanPeriodUnit", 
        null=True, blank=True, related_name="grace_products", 
        db_column="default_grace_period_unit")
    
    amount_currency = models.ForeignKey("core.ConfigCurrency", db_column='currency')
    default_amount = models.DecimalField(decimal_places=4, max_digits=18, default=D(0.0))
    min_amount = models.DecimalField(decimal_places=4, max_digits=18, default=D(0.0))
    max_amount = models.DecimalField(decimal_places=4, max_digits=18, default=D(0.0))

    interest_calculation_method = models.ForeignKey("ConfigInterestCalculationMethod")
    default_interest_rate = models.DecimalField(decimal_places=4, max_digits=6, default=D('0.0'))
    default_interest_rate_unit = models.ForeignKey('ConfigLoanPeriodUnit', related_name="default_interest_rates")
    
    min_interest_rate = models.DecimalField(decimal_places=4, max_digits=6, default=D('0.0'))
    max_interest_rate = models.DecimalField(decimal_places=4, max_digits=6, default=D('0.0'))

    objects = LoanProductQueryset.as_manager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "loan_product"
        verbose_name = "Loan Product"

class LoanProductFee(AuditBase):
    DISBURSEMENT = 0
    REPAYMENT = 1

    CHARGED_AT = (
        (DISBURSEMENT, "Disbursement"),
        (REPAYMENT, "Repayment"),
    )

    product = models.ForeignKey('LoanProduct', related_name="fees")
    charged_at = models.PositiveIntegerField(choices=CHARGED_AT, null=True)
    
    name = models.CharField(max_length=50)
    fee_type = models.ForeignKey('ConfigLoanProductFeeType')
    fee_calculation = models.ForeignKey('ConfigFeeCalculationMethod')

    amount = models.DecimalField(decimal_places=4, max_digits=18, default=D('0.0'))

    def __str__(self):
        return self.name

    class Meta:
        db_table = "loan_product_fee"
        verbose_name = "Loan Fee"
