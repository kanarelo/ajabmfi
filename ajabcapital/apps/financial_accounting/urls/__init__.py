from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

from .banking import BANKING_URLS

from .. import views

urlpatterns = [
    url(r'^accounting/$', views.dashboard, name="dashboard")
]

#1. Add the product urls
urlpatterns += BANKING_URLS