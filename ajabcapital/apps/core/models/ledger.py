from .base import *
from .querysets import *

class LedgerAccount(AuditBase):
    name = models.CharField(max_length=100, unique=True)
    ledger_code = models.CharField(max_length=100, primary_key=True)

    account_category = models.ForeignKey('ConfigLedgerAccountCategory')
    balance_direction = models.ForeignKey('ConfigLedgerAccountBalanceDirection')

    system_defined = models.BooleanField(default=False)

    objects = LedgerAccountQueryset.as_manager()

    def __unicode__(self):
        return "#%s: %s" % (self.ledger_code, self.name)

    class Meta:
        db_table = "ledger_account"
        verbose_name = "Ledger Account"
        ordering = ['ledger_code']

class LedgerAccountingRule(AuditBase):
    transaction_type = models.ForeignKey(
        'ConfigLedgerTransactionType', related_name="accounting_rules"
    )

    debit_account  = models.ForeignKey('LedgerAccount', related_name="debits")
    credit_account = models.ForeignKey('LedgerAccount', related_name="credits")

    system_defined = models.BooleanField(default=False)

    class Meta:
        db_table = "ledger_accounting_rule"
        verbose_name = "Ledger Accounting Rule"

class LedgerTransaction(AuditBase):
    LOAN = 1
    SAVINGS = 2

    PRODUCT_TYPES = (
        (LOAN, "Loan"),
        (SAVINGS, "Savings")
    )

    #the transaction number, it can be random or sequential
    transaction_no = models.CharField(primary_key=True, max_length=15)
    transaction_type = models.ForeignKey('ConfigLedgerTransactionType')

    #The product account is an implicit FK to LoanAccount... This is as this because 
    #this module does not make assumptions, so, that it can be used by diff products.
    product_type = models.PositiveIntegerField(choices=PRODUCT_TYPES, null=True)
    product_account = models.CharField(max_length=25, null=True)

    #which transaction are we reversing if this is a reversal transaction
    reversing_transaction = models.ForeignKey('LedgerTransaction', null=True, blank=True)

    #the amount
    currency = models.ForeignKey("ConfigCurrency", blank=True, null=True)
    amount = models.DecimalField(
        max_digits=18, decimal_places=4, default=D('0.0')
    )

    notes = models.CharField(max_length=500, null=True)
    #if the recepient was notified
    notified = models.NullBooleanField()

    last_status = models.ForeignKey('ConfigLedgerTransactionStatus')
    last_status_date = models.DateTimeField()

    objects = LedgerTransactionQueryset.as_manager()

    class Meta:
        db_table = "ledger_transaction"
        verbose_name = "Ledger Transaction"

    def __unicode__(self):
        return "#%s: %s" % (self.transaction_no, self.transaction_type)

class LedgerTransactionStatus(AuditBase):
    transaction = models.ForeignKey('LedgerTransaction', related_name="statuses")
    transaction_status = models.ForeignKey(
        'ConfigLedgerTransactionStatus'
    )
    transaction_status_date = models.DateTimeField()
    notes = models.CharField(max_length=160)

    class Meta:
        db_table = "ledger_transaction_status"
        verbose_name = "Ledger Transaction Status"
        verbose_name_plural = "Ledger Transaction Statuses"

class LedgerEntry(AuditBase):
    #-------------------------------------------
    (DEBIT, CREDIT) = (0, 1)
    (ITEM_TYPES) = ((DEBIT, 'Debit'), (CREDIT, 'Credit'))
    #-------------------------------------------
    #transaction and ledger account
    ledger_transaction = models.ForeignKey('LedgerTransaction', related_name="entries")
    ledger_account  = models.ForeignKey('LedgerAccount')
    #-------------------------------------------
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

    objects = LedgerEntryQueryset.as_manager()

    class Meta:
        db_table = "ledger_entry"
        verbose_name = "Ledger Entry"
        verbose_name_plural = "Ledger Entries"

# class LedgerBankAccount(ConfigBase):
#     ledger_account = models.ForeignKey('core.LedgerAccount')

#     class Meta:
#         db_table = "bank_account"
