"""
Django settings for ajabcapital project.

Generated by 'django-admin startproject' using Django 1.9.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
from django.core.urlresolvers import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.join(
    '..', os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '?P<SECURITY>_7^2i0##!skpu4cz(nsdsd-m.0.09239028932coxuvx-0(p4&7py-+7aq)@edsdsn$&)@i2-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'ajabcapital.apps.website',
    'ajabcapital.apps.users',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ajabcapital.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ajabcapital.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [{
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    }, {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    }, {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    }, {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    }
]

AUTH_USER_MODEL = "users.User"


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "..", "static"),
)

LOGIN_REDIRECT_URL = '/'

LOGIN_URL = reverse_lazy('login')
DEFAULT_FROM_EMAIL = "Ajab Capital Info <info@ajabcapital.com>"

LOG_ROOT = os.environ.get('LOG_ROOT', os.path.join(BASE_DIR, '..'))

LOGGING = {
    'version': 1,
    'formatters': {
        'simple': {
            'level': 'DEBUG',
            'format': '%(levelname)s %(asctime)s %(message)s',
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'stream': {
            'formatter': 'simple',
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'django_log_file': {
            'level' : 'INFO',
            'class' : 'logging.handlers.RotatingFileHandler',
            'filename' : os.path.join(LOG_ROOT, 'logs', 'django.request.log'),
            'maxBytes' : 1024 * 1024 * 20, # 20MB
            'backupCount' : 10,
            'formatter' : 'simple'
        },
        'core_log_file': {
            'level' : 'INFO',
            'class' : 'logging.handlers.RotatingFileHandler',
            'filename' : os.path.join(LOG_ROOT, 'logs', 'core.log'),
            'maxBytes' : 1024 * 1024 * 20, # 20MB
            'backupCount' : 10,
            'formatter' : 'simple'
        }
    },
    'loggers':  {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'core.ajabcapital': {
            'handlers': ['stream', 'core_log_file'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['stream', 'django_log_file'],
            'propagate': True,
            'level': 'DEBUG',
        },
    }
}