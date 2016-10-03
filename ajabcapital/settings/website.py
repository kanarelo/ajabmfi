from .base import *
import dj_database_url

DEBUG = False

ALLOWED_HOSTS = [
    '.ajabcapital.com',
    'ajabcapital.ajabworld.net',
    '192.241.160.33'
]

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

DATABASES['default'] = dj_database_url(os.environ.get(
    'AJABCAPITAL_WEBSITE_DB_URL', 'sqlite:///../../db/ajabcapital.sqlite3'))

AUTH_USER_MODEL = 'auth.User'

ROOT_URLCONF = 'ajabcapital.apps.website.urls'

try:
	from .local import *
except ImportError:
	pass