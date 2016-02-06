from django.conf.urls import url
from django.contrib import admin

from .views import *

urlpatterns = [
    url(r'^$', index, name="index"),
    url(r'^about-us/$', about_us, name="about-us"),
    url(r'^careers/$', careers, name="careers"),
    url(r'^partners/$', partners, name="partners"),
]
