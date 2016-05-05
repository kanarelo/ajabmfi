from django.conf.urls import include, url
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^dashboard/$', views.dashboard, name="dashboard"),
    url(r'^kyc/$', views.kyc, name="kyc"),
    url(r'^watch-list/$', views.watch_list, name="watch-list"),
    url(r'^liquidity/$', views.liquidity, name="liquidity"),
    url(r'^policies/$', views.policies, name="policies"),
    url(r'^crb-settings/$', views.crb_settings, name="crb-settings"),
]