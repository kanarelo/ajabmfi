from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('ajabcapital.apps.website.urls')),
    url(r'users/', include('ajabcapital.apps.core_users.urls', namespace="users")),
    url(r'risk/', include('ajabcapital.apps.risk_management.urls', namespace="risk-management")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
