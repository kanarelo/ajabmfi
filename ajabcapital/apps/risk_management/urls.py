from django.conf.urls import include, url
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^dashboard/$', views.dashboard, name="dashboard"),
]