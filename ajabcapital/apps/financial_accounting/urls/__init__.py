from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

from .banking import BANKING_URLS

from .. import views

urlpatterns = [
    url(r'^dashboard/$', views.dashboard, name="dashboard"),
    url(r'^balance-sheet/$', views.balance_sheet, name="balance-sheet"),
    url(r'^profit-loss-statement/$', views.pnl_statement, name="pnl-statement"),
    url(r'^general-journal/$', views.general_journal, name="general-journal"),
    url(r'^trial-balance/$', views.trial_balance, name="trial-balance"),
    url(r'^product-ledgers/$', views.product_ledgers, name="product-ledgers"),
    url(r'^banking/$', views.banking, name="banking"),
]

#1. Add the product urls
urlpatterns += BANKING_URLS