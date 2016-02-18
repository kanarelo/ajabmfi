from __future__ import unicode_literals

from django.db import models

from decimal import Decimal as D

from ajabcapital.apps.core.models import AuditBase, ConfigBase

class ConfigGLAccountType(ConfigBase):
    class Meta:
        db_table = "config_gl_account_type"
        verbose_name = "Config GL Account Type"


class ConfigGLTransactionEntryType(ConfigBase):
    class Meta:
        db_table = "config_gl_transaction_entry_type"
        verbose_name = "Config GL Transaction Entry Type"    

class ConfigGLAccountCategory(ConfigBase):
    class Meta:
        db_table = "config_gl_account_category"
        verbose_name = "Config GL Account Category"
        verbose_name_plural = "Config GL Account Categories"

class ConfigGLTransactionStatus(ConfigBase):
    icon = models.FileField(upload_to="config/icons/", null=True, blank=True)

    class Meta:
        db_table = "config_gl_transaction_status"
        verbose_name = "Config GL Transaction Status"
        verbose_name_plural = "Config GL Transaction Statuses"

class GeneralLedgerAccount(AuditBase):
    name = models.CharField(max_length=50)
    gl_code = models.CharField(max_length=25, primary_key=True)

    account_type = models.ForeignKey('ConfigGLAccountType')
    account_category = models.ForeignKey('ConfigGLAccountCategory')

    def __unicode__(self):
        return "#%s: %s" % (self.gl_code, self.name)

    class Meta:
        db_table = "general_ledger_account"
        verbose_name = "General Ledger Account"

class GeneralLedgerTransaction(AuditBase):
    status = models.ForeignKey('ConfigGLTransactionStatus')

    currency = models.ForeignKey("core.ConfigCurrency", blank=True, null=True)
    amount = models.DecimalField(
        max_digits=18, decimal_places=4, default=D('0.0')
    )

    entry_type = models.ForeignKey('ConfigGLTransactionEntryType')

    notes = models.CharField(max_length=160, null=True)

    class Meta:
        db_table = "general_ledger_transaction"
        verbose_name = "General Ledger Transaction"

class GeneralLedgerTransactionEntry(AuditBase):
    CREDIT = 0
    DEBIT  = 1

    ITEM_TYPE = (
        (CREDIT, 'Credit'),
        (DEBIT, 'Debit'),
    )

    transaction = models.ForeignKey('GeneralLedgerTransaction')
    item_type = models.PositiveIntegerField(choices=ITEM_TYPE)

    gl_code = models.CharField(max_length=25, null=True)

    ledger_balance_increment = models.DecimalField(
        max_digits=18, decimal_places=4, default=D(0.0)
    )

    class Meta:
        db_table = "general_ledger_transaction_entry"
        verbose_name = "General Ledger Transaction Entry"
        verbose_name = "General Ledger Transaction Entries"
