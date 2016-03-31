from django.conf.urls import url
from django.contrib import admin

from .views import *

urlpatterns = [
    url(r'^dashboard/$', dashboard, name="dashboard"),
    url(r'^main-menu/$', main_menu, name="main_menu"),
    url(r'^notifications/$', notifications, name="notifications"),
    

]