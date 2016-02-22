from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from decimal import Decimal as D

class AuditBase(models.Model):
    row_comment = models.CharField(max_length=250, null=True, blank=True)

    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="%(app_label)s_%(class)s_deleted_by_me",
        null=True, blank=True, db_column="deleted_by"
    )

    is_deleted = models.BooleanField(default=False)
    date_deleted = models.DateTimeField(null=True, blank=True)
    reason_deleted = models.CharField(max_length=250, null=True, blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="%(app_label)s_%(class)s_created_by_me",
        null=False, db_column="created_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class ConfigBase(AuditBase):
    '''Class Account Closure Reason'''
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    is_active = models.BooleanField(default=True)
    
    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

#------------------------------------------------------

class ConfigBalanceClosureType(ConfigBase):
    class Meta:
        db_table = "config_balance_closure_type"
        verbose_name = "Config Balance Closure Type"

class ConfigCurrency(ConfigBase):
    class Meta:
        db_table = "config_currency"
        verbose_name = "Config Currency"
        verbose_name_plural = "Config Currencies"

class ConfigLedgerAccountType(ConfigBase):
    icon = models.FileField(upload_to="config/icons/", null=True, blank=True)

    class Meta:
        db_table = "config_ledger_account_type"
        verbose_name = "Config Ledger Account Type"

class ConfigLedgerAccountCategory(ConfigBase):
    icon = models.FileField(upload_to="config/icons/", null=True, blank=True)

    class Meta:
        db_table = "config_ledger_account_category"
        verbose_name = "Config Ledger Account Category"
        verbose_name_plural = "Config Ledger Account Categories"

class ConfigLedgerType(ConfigBase):
    class Meta:
        db_table = "config_ledger_type"
        verbose_name = "Config Ledger Type"

class ConfigLedgerTransactionType(ConfigBase):
    icon = models.FileField(upload_to="config/icons/", null=True, blank=True)
    ledger_types = models.ManyToManyField('ConfigLedgerType')

    class Meta:
        db_table = "config_ledger_transaction_type"
        verbose_name = "Config Ledger Transaction Type"    

class ConfigLedgerTransactionStatus(ConfigBase):
    icon = models.FileField(upload_to="config/icons/", null=True, blank=True)

    class Meta:
        db_table = "config_ledger_transaction_status"
        verbose_name = "Config Ledger Transaction Status"
        verbose_name_plural = "Config Ledger Transaction Statuses"

class LedgerAccount(AuditBase):
    name = models.CharField(max_length=50, unique=True)
    ledger_code = models.CharField(max_length=25, primary_key=True)

    ledger_type = models.ForeignKey('ConfigLedgerType')
    account_type = models.ForeignKey('ConfigLedgerAccountType', default=1)
    account_category = models.ForeignKey('ConfigLedgerAccountCategory')

    def __unicode__(self):
        return "#%s: %s" % (self.ledger_code, self.name)

    class Meta:
        db_table = "ledger_account"
        verbose_name = "Ledger Account"

class LedgerTransaction(AuditBase):
    transaction_no = models.CharField(primary_key=True, max_length=15)
    transaction_type = models.ForeignKey('ConfigLedgerTransactionType')
    transaction_status = models.ForeignKey('ConfigLedgerTransactionStatus')

    currency = models.ForeignKey("core.ConfigCurrency", blank=True, null=True)
    amount = models.DecimalField(
        max_digits=18, decimal_places=4, default=D('0.0')
    )

    notes = models.CharField(max_length=500, null=True)
    notified = models.BooleanField(default=False)

    class Meta:
        db_table = "ledger_transaction"
        verbose_name = "Ledger Transaction"

class LedgerEntry(AuditBase):
    CREDIT = 0
    DEBIT  = 1

    ITEM_TYPE = (
        (CREDIT, 'Credit'),
        (DEBIT, 'Debit'),
    )

    ledger_account = models.ForeignKey('LedgerAccount')
    ledger_transaction = models.ForeignKey('LedgerTransaction')

    ledger_balance_item_type = models.PositiveIntegerField(choices=ITEM_TYPE)
    ledger_balance_increment = models.DecimalField(
        max_digits=18, decimal_places=4, default=D(0.0)
    )

    class Meta:
        db_table = "ledger_entry"
        verbose_name = "Ledger Entry"
        verbose_name_plural = "Ledger Entries"

class LedgerBalanceRegister(AuditBase):
    ledger_account = models.ForeignKey('LedgerAccount')
    balance_closure_type   = models.ForeignKey('ConfigBalanceClosureType')

    balance_amount = models.DecimalField(
        max_digits=18, decimal_places=4, default=D('0.0')
    )
    balance_as_at  = models.DateTimeField()

    class Meta:
        db_table = "ledger_balance"
        verbose_name = verbose_name_plural= "Ledger Balance Register"
