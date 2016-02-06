from .base import *

DEBUG = False

SECRET_KEY = '98tghjcfhv.U.O.I09237923bhjasUYVX98a02372--u2hj3mashjbsambcIII}|bjas,j%0y#q#nmb*d%u(#'
ALLOWED_HOSTS = [
    '.ajabcapital.com',
    '192.241.160.33'
]

# # Database
# # https://docs.djangoproject.com/en/1.7/ref/settings/#databases
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'ajabcapital',
#         'USER': 'ajabcapital',
#         'PASSWORD': 'o94u3n3jJJKS21032sjdu34nsnlp223'
#     }
# }

BASE_URL = 'http://www.ajabcapital.com'

STATIC_ROOT = '/opt/apps/assets/ajabcapital/static/'
MEDIA_ROOT = '/opt/apps/assets/ajabcapital/media/'

# Use local settings if it's available

try:
    from .local import *
except ImportError:
    pass