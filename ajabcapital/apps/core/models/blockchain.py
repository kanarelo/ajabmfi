from .base import *

class LedgerTransactionBlock(BaseTransactionBlock):
    '''
    This ledger is for high level, accounts, those that are defined by the system.
    Blocks record and confirm when and in what sequence 
    transactions enter and are logged in the block chain.
    '''
    class Meta:
        db_table = "ledger_transaction_block"
        verbose_name = "Ledger Transaction Block"

class LedgerTransactionBlockItem(BaseTransactionBlockItem):
    '''
    '''
    LOAN = 1
    SAVINGS = 2

    PRODUCT_TYPES = (
        (LOAN, "Loan"),
        (SAVINGS, "Savings")
    )
    product_type = models.PositiveIntegerField(choices=PRODUCT_TYPES, default=LOAN)

    block = models.ForeignKey('LedgerTransactionBlock', related_name="block_items")
    ledger_account = models.ForeignKey('LedgerAccount')
    
    product_account = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = "ledger_transaction_block_item"
        verbose_name = "Ledger Transaction Block Item"

    def __unicode__(self):
        return "#{0} {1} KES. {2:.2f} as at {3} {4}".format(
            self.block.block_id, 
            self.ledger_account, 
            self.balance_amount,
            self.block.balances_as_at.strftime("%Y-%m-%d %H:%M"),
            self.product_account if not None else "",
        )
