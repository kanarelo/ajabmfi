from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

from .. import views

PRODUCTS_URLS = [
	url(r'^product/create/', views.create_product, name="create-product"),
	url(r'^product/edit/', views.edit_product, name="edit-product"),
]