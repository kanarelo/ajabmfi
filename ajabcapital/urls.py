from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('ajabcapital.apps.website.urls')),
    url(r'home/', include('ajabcapital.apps.core.urls', namespace="home")),
    url(r'users/', include('ajabcapital.apps.core_users.urls', namespace="users")),
    url(r'loans/', include('ajabcapital.apps.loan.urls', namespace="loans")),
    url(r'risk-and-compliance/', include('ajabcapital.apps.risk_management.urls', namespace="risk")),
    url(r'clients/', include('ajabcapital.apps.crm.urls', namespace="crm")),
    url(r'accounting/', include('ajabcapital.apps.financial_accounting.urls', namespace="accounting")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
