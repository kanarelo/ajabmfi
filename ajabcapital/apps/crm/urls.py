from django.conf.urls import url
from django.contrib import admin

from .views import *

urlpatterns = [
    url(r'^dashboard/$', dashboard, name="dashboard"),
    url(r'^search_client/$', search_client, name="search_client"),
]