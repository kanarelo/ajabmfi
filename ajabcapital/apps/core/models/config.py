from .base import *

class ConfigBlockType(ConfigBase):
    class Meta:
        db_table = "config_block_type"
        verbose_name = "Config Block Type"

class ConfigCurrency(ConfigBase):
    class Meta:
        db_table = "config_currency"
        verbose_name = "Config Currency"
        verbose_name_plural = "Config Currencies"

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

class ConfigLedgerTransactionType(ConfigBase):
    icon = models.FileField(upload_to="config/icons/", null=True, blank=True)
    posts_to_ledger = models.BooleanField(default=True)

    class Meta:
        db_table = "config_ledger_transaction_type"
        verbose_name = "Config Ledger Transaction Type"    

class ConfigLedgerTransactionStatus(ConfigBase):
    icon = models.FileField(upload_to="config/icons/", null=True, blank=True)

    class Meta:
        db_table = "config_ledger_transaction_status"
        verbose_name = "Config Ledger Transaction Status"
        verbose_name_plural = "Config Ledger Transaction Statuses"
