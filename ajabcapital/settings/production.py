from .base import *

DEBUG = False

SECRET_KEY = '98t$^^**-773-gh687tetiu_ysgdjh-cgkg|t37---0u2hj3mashjbsambcIII}|bjas,j%0y#q#nmb*d%u(#OOOOO'
ALLOWED_HOSTS = [
    '.ajabcapital.net'
]

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django',
        'USER': 'django',
        'PASSWORD': '598bab6dffcf25833841fa123df676bc'
    }
}

BASE_URL = 'http://www.ajabcapital.com'
# Use local settings if it's available

try:
    from .local import *
except ImportError:
    pass