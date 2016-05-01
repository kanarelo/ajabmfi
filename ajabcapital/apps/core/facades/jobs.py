from .transactions import *
from .blockchain import *

from ..utils import *
from ...core_users.models import *

def close_ledger_accounts():
    time_closed = timezone.now()
    user = User.objects.get(pk=3)

    GENERAL_LEDGER = "LGT_001"

    def get_chart_of_accounts():
        account_categories = ConfigLedgerAccountCategory.objects.filter(
            is_active=True
        )
        account_categories_dict = {}

        for account_category in account_categories:
            account_categories_dict[account_category.code] = (
                LedgerAccount.objects.filter(
                    account_category=account_category
                ).order_by('ledger_code').only('name', 'ledger_code')
            )

        return account_categories_dict

    def get_next_block():
        return LedgerTransactionBlock.objects.create(
            name="Automatic end of Day closures",
            notes="%s @ %s" % ("Automatic end of Day closures", time_closed),
            balances_as_at=time_closed,
            created_by=user,
            block_id=get_reference_no(15)
        )

    #get the next block & chart of accounts
    block = get_next_block()
    chart_of_accounts = get_chart_of_accounts()

    #Loop through the ledger accounts
    for (account_category, ledger_accounts_queryset) in chart_of_accounts.iteritems():
        #loop through the ledger_account's
        for ledger_account in ledger_accounts_queryset:
            print close_ledger_account(ledger_account, block, user=user)
