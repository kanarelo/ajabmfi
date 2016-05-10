from django.db import models

from ..core.models import ConfigBase, AuditBase

# --------------------
# 1.0000.0000 - level0
# 1.1000.0000 - level1
# 1.1100.0000 - level2
# 1.1110.0000 - level3
# 1.1111.0000 - level4
# 1.1111.1000 - level5
# 1.1111.1100 - level6
# 1.1111.1110 - level7
# 1.1111.1111 - level8
# --------------------

class ConfigBankingPartnerSector(ConfigBase):
    class Meta:
        db_table = "config_banking_partner_sector"

class ConfigBankingPartner(ConfigBase):
    icon = models.FileField(upload_to="icon/banks")
    partner_sector = models.ForeignKey('ConfigBankingPartnerSector')

    class Meta:
        db_table = "config_banking_partner"

class BankAccount(AuditBase):
    name = models.CharField(max_length=100)

    partner = models.ForeignKey('ConfigBankingPartner')
    ledger_account = models.ForeignKey('core.LedgerAccount')

    bank_account_number = models.CharField(max_length=100)

    class Meta:
        db_table = "bank_account"
        unique_together = ('bank_account_number', 'partner')
