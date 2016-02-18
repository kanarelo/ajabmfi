from .base import *

DEBUG = False

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'bootstrap3',

    'ajabcapital.apps.website'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '../../db/landing.db',
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ajabcapital',
        'USER': 'ajabcapital',
        'PASSWORD': 'qoSQhO5ygV'
    }
}

AUTH_USER_MODEL = 'auth.User'

ROOT_URLCONF = 'ajabcapital.apps.website.urls'

try:
	from .local import *
except ImportError:
	pass