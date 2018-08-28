"""
Django settings for aucarvideo project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-%+&==jfv2cbm_n-+8j^e^xx3i09=-$4+3h)kd(nb!tz+xv2gd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

TENANT_MODEL = "customers.Client" # app.Model

# This variable was created to give this domain name 
# to all tenants created
DOMAIN_NAME = 'aucarvideo'

# Mail settings
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = "587"
EMAIL_HOST_USER = os.environ.get('AUCARVIDEO_EMAIL','')
EMAIL_HOST_PASSWORD = os.environ.get('AUCARVIDEO_PASSWORD','')
EMAIL_USE_TLS = True

# Application definition

# These apps models will be created in the public schema 
SHARED_APPS = (
    'tenant_schemas',  # mandatory, should always be before any django app

    # everything below here is optional
    'customers',
    'home_public',

    # django apps
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
)

# This apps models will be replicated in schemas
TENANT_APPS = (
    # your tenant-specific apps
    
    # 'login',
    'auth_tenants',
    'home_tenants',
    'contests',

    # django apps
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
)

INSTALLED_APPS = (
    'tenant_schemas',  # mandatory, should always be before any django app

    # your tenant-specific apps
    'customers',
    'home_public',
    'auth_tenants',
    'home_tenants',
    'contests',
    # 'login',
    # 'home_tenats',


    # django apps
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    # 'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',

    # To serve django admin staticfiles
    'django.contrib.staticfiles',

    # Others  Apps
    'bootstrap3',
)

# For django-tenant-schemas
# Add the middleware tenant_schemas.middleware.TenantMiddleware 
# to the top of MIDDLEWARE_CLASSES, so that each request can be 
# set to use the correct schema.

MIDDLEWARE = [
    # For django-tenant-schemas
    'tenant_schemas.middleware.TenantMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ROOT_URLCONF = 'aucarvideo.urls'
ROOT_URLCONF = 'aucarvideo.urls_tenants'
PUBLIC_SCHEMA_URLCONF = 'aucarvideo.urls_public'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,  'templates')],
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

WSGI_APPLICATION = 'aucarvideo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
    'ENGINE': 'tenant_schemas.postgresql_backend',
    'NAME': 'postgres',
    'USER': 'postgres', 
    'PASSWORD': 'postgres',
    'HOST': '172.17.0.2',
    'PORT': '5432',
    }
}

# Add tenant_schemas.routers.TenantSyncRouter to your DATABASE_ROUTERS setting, 
# so that the correct apps can be synced, depending on what’s being synced (shared or tenant).
DATABASE_ROUTERS = (
    'tenant_schemas.routers.TenantSyncRouter',
)

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'es-co'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
]


# The storage API will not isolate media per tenant. 
# Your MEDIA_ROOT will be a shared space between all tenants.

# To avoid this you should configure a tenant aware storage
# backend - you will be warned if this is not the case.
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
