"""
Django settings for autocry project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from os.path import join
from pathlib import Path

# Heroku settings
import django_heroku
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=p#&$izoov^3=m-7%q-_k*^-)z55p)3f%j0+vr3$pw$y@t*kw='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition

# Console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Insert real mail service settings here

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',
    'django.contrib.staticfiles',

    'rest_framework',
    'django_cleanup',
    'bootstrap4',

    'boto',
    # Avoid 'storages' & 'cloudinary' collectstatic errors by: heroku config:set DISABLE_COLLECTSTATIC=1
    # https://www.dothedev.com/blog/heroku-django-store-your-uploaded-media-files-for-free/
    'cloudinary',
    # 'storages',

    'main_app',
    'auth_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'autocry.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'autocry.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# Heroku settings
DATABASES = {
    'default': dj_database_url.config(),
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

try:
    from .local_settings import *
except ImportError:
    pass

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# STATIC_ROOT = '/tmp/static'    # local directory

MEDIA_ROOT = join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'

LOGIN_URL = '/auth_app/login/'

# Heroku settings
django_heroku.settings(locals())

# Use cloudinary as media storage
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'hewtsbisw',
    'API_KEY': '192825189237136',
    'API_SECRET': 'FiHHpJtfFx5HjGCJlkbmzhLvTu0',
}

# Activate for Heroku upload
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
