from .accounting import ACCOUNTING_URLS
from .accounts import ACCOUNTS_URLS
from .config import CONFIG_URLS
from .products import PRODUCTS_URLS
from .transactions import TRANSACTIONS_URLS
from .webhooks import WEBHOOKS_URLS

urlpatterns = []

#1. Add the product urls
urlpatterns += PRODUCTS_URLS

#2. Add the account urls
urlpatterns += ACCOUNTS_URLS

#3. Add the accounting urls
urlpatterns += ACCOUNTING_URLS

#4. Add the config urls
urlpatterns += CONFIG_URLS

#4. Add the webhook urls
urlpatterns += WEBHOOKS_URLS

#4. Add the webhook urls
urlpatterns += TRANSACTIONS_URLS