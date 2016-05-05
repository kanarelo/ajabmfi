from django.conf.urls import url
from django.contrib import admin

from .views import *

urlpatterns = [
    url(r'^start/$', start, name="start"),
    url(r'^apply/(?P<product_pk>\d+)/$', apply_product, name="apply-product"),
    url(r'^loan-terms/$', loan_terms, name='set-loan-terms'),
    url(r'^loan-processing/$', loan_processing, name='loan-processing'),
]