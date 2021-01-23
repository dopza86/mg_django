"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'oz$&xv-ttrty58%jbckw&piqwqb$r&_6me=u$g&=o&qaq%%ym+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

PROJECT_APPS = [
    "core.apps.CoreConfig",
    "users.apps.UsersConfig",
    "posts.apps.PostsConfig",
    "likes.apps.LikesConfig",
    "follow_relation.apps.FollowRelationConfig",
    "comments.apps.CommentsConfig",
    "conversations.apps.ConversationsConfig",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "import_export",
    "taggit",
    "taggit_serializer",
    "django_seed",
    "rest_auth",
    'rest_framework.authtoken',
    'rest_auth.registration',
    'allauth',
    "corsheaders",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")

MEDIA_URL = "/media/"

# Auth
AUTH_USER_MODEL = "users.User"

# Django Rest Framework

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS':
    'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE':
    10,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "config.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
}

MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")
MEDIA_URL = "/media/"

# 이메일 설정

EMAIL_HOST = "smtp.mailgun.org"
EMAIL_PORT = "587"

EMAIL_HOST_USER = os.environ.get("MAILGUN_USERNAME")
EMAIL_HOST_PASSWORD = os.environ.get("MAILGUN_PASSWORD")

EMAIL_FROM = "noreply@sandbox1eef570fd7ee4a9ca110f0f2fad9115e.mailgun.org"

# rest_auth

REST_USE_JWT = True
OLD_PASSWORD_FIELD_ENABLED = True
ACCOUNT_LOGOUT_ON_GET = True

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = True