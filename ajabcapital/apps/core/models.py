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
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    is_active = models.BooleanField(default=True)
    
    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

#------------------------------------------------------

class ConfigBlockType(ConfigBase):
    class Meta:
        db_table = "config_block_type"
        verbose_name = "Config Block Type"

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

class ConfigLedgerAccountBalanceDirection(ConfigBase):
    icon = models.FileField(upload_to="config/icons/", null=True, blank=True)

    class Meta:
        db_table = "config_ledger_account_balance_direction"
        verbose_name = "Config Ledger Balance Direction"

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

#------------------------------------------------------------------------------

class LedgerAccount(AuditBase):
    name = models.CharField(max_length=50, unique=True)
    ledger_code = models.CharField(max_length=100, primary_key=True)

    ledger_type = models.ForeignKey('ConfigLedgerType')
    account_category = models.ForeignKey('ConfigLedgerAccountCategory')
    account_type = models.ForeignKey('ConfigLedgerAccountType', default=1)
    balance_direction = models.ForeignKey('ConfigLedgerAccountBalanceDirection')

    def __unicode__(self):
        return "#%s: %s" % (self.ledger_code, self.name)

    class Meta:
        db_table = "ledger_account"
        verbose_name = "Ledger Account"

class LedgerAccountingRule(AuditBase):
    transaction_type = models.ForeignKey(
        'ConfigLedgerTransactionType', related_name="accounting_rules"
    )

    debit_account  = models.ForeignKey('LedgerAccount', related_name="debits")
    credit_account = models.ForeignKey('LedgerAccount', related_name="credits")

    class Meta:
        db_table = "ledger_accounting_rule"
        verbose_name = "Ledger Accounting Rule"

class LedgerTransaction(AuditBase):
    #the transaction number, it can be random or sequential
    transaction_no = models.CharField(primary_key=True, max_length=15)
    transaction_type = models.ForeignKey('ConfigLedgerTransactionType')

    #The product account is an implicit FK to LoanAccount... This is as this because 
    #this module does not make assumptions, so, that it can be used by diff products.
    product_account = models.CharField(max_length=25, null=True)

    #which transaction are we reversing if this is a reversal transaction
    reversing_transaction = models.ForeignKey('LedgerTransaction', null=True)

    #the amount
    currency = models.ForeignKey("ConfigCurrency", blank=True, null=True)
    amount = models.DecimalField(
        max_digits=18, decimal_places=4, default=D('0.0')
    )

    notes = models.CharField(max_length=500, null=True)
    #if the recepient was notified
    notified = models.NullBooleanField()

    last_status = models.ForeignKey('LedgerTransactionStatus')
    last_status_date = models.DateTimeField()

    class Meta:
        db_table = "ledger_transaction"
        verbose_name = "Ledger Transaction"

class LedgerEntry(AuditBase):
    #-------------------------------------------
    (DEBIT, CREDIT) = (0, 1)
    (ITEM_TYPES) = ((DEBIT, 'Debit'), (CREDIT, 'Credit'))
    #-------------------------------------------

    #-------------------------------------------
    #transaction and ledger account
    ledger_transaction = models.ForeignKey('LedgerTransaction', related_name="entries")
    ledger_account  = models.ForeignKey('LedgerAccount')
    #-------------------------------------------
    #duplicate of what we have in the transaction... for analytics...
    product_account = models.CharField(max_length=25, null=True)

    #debit or credit... According to the account type, and item type, we affect ledger_balance_increment
    ledger_balance_item_type = models.PositiveIntegerField(choices=ITEM_TYPES)

    #------------------------------------------------------------
    # The change in balance of ledger account according 
    # to *item type*, *account type*, and *balance direction*:
    #------------------------------------------------------------
    # a DEBIT is an accounting entry that either 
    # increases an asset or expense account, or 
    # decreases a liability or equity account.
    #-------------------------------------------
    # a CREDIT is an accounting entry that either 
    # increases a liability or equity account, or 
    # decreases an asset or expense account.
    #-------------------------------------------
    # Also, if its a CONTRA account, balances are negated further.
    ledger_balance_increment = models.DecimalField(
        max_digits=18, decimal_places=4, default=D(0.0)
    )

    class Meta:
        db_table = "ledger_entry"
        verbose_name = "Ledger Entry"
        verbose_name_plural = "Ledger Entries"

class LedgerTransactionStatus(AuditBase):
    transaction = models.ForeignKey('LedgerTransaction')
    transaction_status = models.ForeignKey(
        'ConfigLedgerTransactionStatus', related_name="statuses"
    )
    transaction_status_date = models.DateTimeField()
    notes = models.CharField(max_length=160)

    class Meta:
        db_table = "ledger_transaction_status"
        verbose_name = "Ledger Transaction Status"
        verbose_name_plural = "Ledger Transaction Statuses"

#---------------------------------------------------------------
# Balances are closed to avoid post dating, thus, we can't introduce more
# transactions. We are experimenting around the Blockchain.

class LedgerTransactionBlock(AuditBase):
    block_id = models.CharField(max_length=100, primary_key=True)

    name = models.CharField(max_length=100)
    notes = models.CharField(max_length=160)

    block_type   = models.ForeignKey('ConfigBlockType')
    balances_as_at  = models.DateTimeField()

    class Meta:
        db_table = "ledger_transaction_block"
        verbose_name = "Ledger Transaction Block"

class LedgerTransactionBlockItem(AuditBase):
    block = models.ForeignKey('LedgerTransactionBlock', related_name="block_items")

    ledger_account  = models.ForeignKey('LedgerAccount')
    balance_amount  = models.DecimalField(max_digits=18, decimal_places=4, default=D('0.0'))

    class Meta:
        db_table = "ledger_transaction_block_item"
        verbose_name = "Ledger Transaction Block Item"

class LedgerProductBlockItem(AuditBase):
    block = models.ForeignKey('LedgerTransactionBlock', related_name="product_block_items")

    product_account = models.CharField(max_length=25)
    balance_amount  = models.DecimalField(max_digits=18, decimal_places=4, default=D('0.0'))

    class Meta:
        db_table = "product_account_block_item"
        verbose_name = "Ledger Product Block Item"
