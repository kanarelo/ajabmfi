from django.conf.urls import url
from django.contrib import admin

from .views import *

urlpatterns = [
    url(r'^dashboard/$', dashboard, name="dashboard"),
    url(r'^my-pipeline/$', my_pipeline, name="my_pipeline"),
    url(r'^reports/$', reports, name="home_reports"),
]