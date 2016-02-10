from .base import *

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'ajabcapital.apps.website.apps.WebsiteConfig'
]

try:
	from .local import *
except ImportError:
	pass