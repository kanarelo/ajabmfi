from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

from .. import views

ACCOUNTS_URLS = [
    # url(r'^accounts/transactions/$', views.repay_account, name="repay-loan-account"),
    # url(r'^accounts/status/change/$', views.create_account, name="change-status-account"),
    # url(r'^accounts/edit/$', views.edit_account, name="edit-account"),
    # url(r'^accounts/view/$', views.view_account, name="view-account"),

    # url(r'^accounts/repay/$', views.repay_account, name="repay-loan-account"),
    # url(r'^accounts/disburse/$', views.disburse_loan_account, name="disburse-loan-account"),
    # url(r'^accounts/schedule/$', views.account_amortization_schedule, name="loan-account-schedule"),

    # url(r'^accounts/disburse/$', views.disburse_loan_account, name="disburse-loan-account"),
    # url(r'^accounts/schedule/$', views.account_amortization_schedule, name="loan-account-schedule"),
]