from __future__ import unicode_literals

from django.db import models

from decimal import Decimal as D

from ajabcapital.apps.core.models import AuditBase, ConfigBase

class LoanProduct(AuditBase):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=140)
    is_active = models.BooleanField(default=False)

    loan_type = models.ForeignKey('ConfigLoanProductType')
    period_unit = models.ForeignKey("ConfigLoanPeriodUnit")
    grace_period_type = models.ForeignKey("ConfigGracePeriodType", null=True, blank=True)
    interest_calculation_method = models.ForeignKey("ConfigInterestCalculationMethod")
    
    default_repayment_period = models.IntegerField(default=0)
    default_grace_period = models.IntegerField(default=0)

    currency = models.ForeignKey("core.ConfigCurrency", blank=True, null=True)

    min_amount = models.DecimalField(decimal_places=4, max_digits=18, default=D(0.0))
    max_amount = models.DecimalField(decimal_places=4, max_digits=18, default=D(0.0))

    min_installments = models.IntegerField(null=True, blank=False)
    max_installments = models.IntegerField(null=True, blank=False)

    min_interest_rate = models.DecimalField(decimal_places=4, max_digits=6, default=D('0.0'))
    default_interest_rate = models.DecimalField(decimal_places=4, max_digits=6, default=D('0.0'))
    max_interest_rate = models.DecimalField(decimal_places=4, max_digits=6, default=D('0.0'))

    def __str__(self):
        return self.name

    class Meta:
        db_table = "loan_product"
        verbose_name = "Loan Product"

class LoanProductFee(AuditBase):
    name = models.CharField(max_length=50)
    product = models.ForeignKey('LoanProduct', related_name="fees")
    
    fee_type = models.ForeignKey('ConfigLoanProductFeeType')
    fee_calculation = models.ForeignKey('ConfigFeeCalculationMethod')

    amount = models.DecimalField(decimal_places=4, max_digits=18, default=D('0.0'))

    def __str__(self):
        return self.name

    class Meta:
        db_table = "loan_product_fee"
        verbose_name = "Loan Fee"
