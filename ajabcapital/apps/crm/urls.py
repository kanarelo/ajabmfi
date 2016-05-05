from django.conf.urls import url
from django.contrib import admin

from .views import *

urlpatterns = [
    url(r'^overview/$', dashboard, name="dashboard"),
    url(r'^search_client/$', search_client, name="search_client"),
    url(r'^individuals/$', individuals, name="individual_profiles"),
    url(r'^businesses/$', businesses, name="business_profiles"),
    url(r'^groups/$', groups, name="group_profiles"),
    url(r'^messages/$', messages, name="messages"),
    url(r'^campaigns/$', campaigns, name="campaigns"),
    url(r'^applications/$', applications, name="applications"),
    url(r'^templates/$', templates, name="templates"),
]