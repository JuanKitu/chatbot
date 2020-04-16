"""
Django settings for chatbot project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os.path import join
import dj_database_url
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+e2n*2q^4z3ep&%mx26iyx%@!17++g%$0gq%4cnh45ay-#_#u8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'django.contrib.auth.mixins',
    'chatbot',
    'appdiccionario',
    'appdocumentos',
    'appkeywords',
    'apppredefinidas',
    'appsinonimos',
    'apparticulos',
    'appusuarios',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
 #   'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'chatbot.urls'

WSGI_APPLICATION = 'chatbot.wsgi.application'


# Database
# https://docs.djangoprosject.com/en/1.7/ref/settings/#databases

DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'NAME': 'ptah',
         'USER': 'postgres',
         'PASSWORD': 'investigacion',
         'HOST': 'localhost',
         'PORT': '5432',
     }
 }

# if 'DATABASE_URL' does no exist, then it's local machine
if ('DATABASE_URL') in os.environ:
    DATABASES = {'default': dj_database_url.config(default=os.environ['DATABASE_URL'])}



# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = True

DATE_INPUT_FORMATS = ['%d/%m/%Y', '%d-%m-%Y']
DATE_FORMAT = 'd/m/Y'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates').replace('\\','/'),
)
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static').replace('\\','/'),
)

STATIC_URL = '/static/'

SESSION_ENGINE="django.contrib.sessions.backends.signed_cookies"

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ptah.chatbot@gmail.com'
EMAIL_HOST_PASSWORD = 'iwishthiswererandom'

CONTACT_DESTINATIONS=['rafaelmalgor@gmail.com','andrespascal2003@yahoo.com.ar']
LOGIN_REDIRECT_URL = reverse_lazy('home')
LOGOUT_REDIRECT_URL = reverse_lazy('login')