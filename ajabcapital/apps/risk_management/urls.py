from django.conf.urls import include, url
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^dashboard/$', views.dashboard, name="dashboard"),
    url(r'^dashboard/$', views.dashboard, name="kyc"),
    url(r'^dashboard/$', views.dashboard, name="watch-list"),
    url(r'^dashboard/$', views.dashboard, name="liquidity"),
    url(r'^dashboard/$', views.dashboard, name="policies"),
    url(r'^dashboard/$', views.dashboard, name="dashboard"),
]