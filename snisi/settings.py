#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

"""
Django settings for snisi project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^&s&^g3k24=ppc%a77$b@^5ri03ai25d)=0wk@3+r**7!_8q!p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost']


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'iso8601': {
            'handlers': ['null'],
            'level': 'DEBUG',
            'propagate': False,
        },
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}



# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'reversion',
    'south',

    'snisi_core',
    'snisi_web',
    'snisi_tools',
    'snisi_sms',
    'snisi_malaria',

    'snisi_trachoma',
    # 'snisi_reprohealth',
    # 'snisi_bednets',
    # 'snisi_epidemiology',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "snisi_web.processors.branding",
)


ROOT_URLCONF = 'snisi.urls'

WSGI_APPLICATION = 'snisi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

gettext = lambda s: s
LANGUAGES = (('fr', gettext("French")),)
LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'


#
#
#

# DEFAULT_LOCALE = 'fr_FR.UTF-8'

SITE_ID = 1

EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_SENDER = 'root@localhost'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

HOTLINE_NUMBER = "00000000"
HOTLINE_EMAIL = "root@localhost"

SUPPORT_CONTACTS = {
    'unknown': {'name': "HOTLINE", 'email': HOTLINE_EMAIL},
}

USE_HTTPS = False

SYSTEM_CLOSED = False

AUTH_USER_MODEL = 'snisi_core.Provider'

ADMIN_PASSWORD = 'admin'

ALLOWED_HOSTS = ['localhost',
                 'snisi.sante.gov.ml',
                 'snisi2.yeleman.com']


ORANGE = 'orange'
MALITEL = 'malitel'
FOREIGN = 'foreign'
OPERATORS = {ORANGE: ("Orange MALI", [7, 9, 4, 8, 90, 91]),
             MALITEL: ("Malitel", [2, 6, 98, 99]),
             FOREIGN: ("Extérieur", [])}

SMS_CONVERT_UNICODE_TO_ASCII = False

SERVE_PROTECTED_FILES = False
FILES_REPOSITORY_URL_PATH = '/protected'
FILES_REPOSITORY = os.path.join(BASE_DIR, 'protected')

try:
    from snisi.settings_local import *
except ImportError:
    pass
