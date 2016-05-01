from __future__ import unicode_literals

from django.contrib.postgres.fields import JSONField
from django.db import models

from decimal import Decimal as D

from ajabcapital.apps.core.models import (
    AuditBase, 
    ConfigBase, 
    BaseTransactionBlock, 
    BaseTransactionBlockItem
)

class LoanRepaymentAllocationOrder(AuditBase):
    allocation_item = models.ForeignKey('ConfigRepaymentAllocationItem')
    rank = models.PositiveIntegerField()

    class Meta:
        db_table = "loan_repayment_allocation_order"
        verbose_name = "Loan Repayment Allocation Order"

    def __str__(self):
        return "(%s) %s" % (self.product.name, self.allocation_item.name)

class LoanChartOfAccounts(ConfigBase):
    class Meta:
        db_table = "loan_chart_of_accounts"