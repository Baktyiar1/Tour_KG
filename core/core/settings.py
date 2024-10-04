"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path

from decouple import config

from dotenv import load_dotenv
load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = config('SECRET_KEY')
SECRET_KEY = 'django-insecure-jy_b@17qceno3hx!_or^vy=p&rw6_dvz+=##73k47mh!g5!34t'
# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = config('DEBUG', default=False, cast=bool)
DEBUG = True
#
ALLOWED_HOSTS = ['*']

# try:
#     SECRET_KEY = config('SECRET_KEY')
#     print("SECRET_KEY загружен успешно")
# except Exception as e:
#     print("Ошибка загрузки SECRET_KEY:", e)

# print("Available Environment Variables:")
# for key in os.environ.keys():
#     print(key)
# print("SECRET_KEY:", os.getenv('SECRET_KEY'))
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',
    'rest_framework',
    'rest_framework.authtoken',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',

    'drf_yasg',
    'corsheaders',

# locals app
    'tour',
    'user',
    'qrcode',

    'django_filters',
]



MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

# django.contrib.sites
SITE_ID = 1

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('DB_NAME'),
#         'USER': config('DB_USER'),
#         'PASSWORD': config('DB_PASSWORD'),
#         'HOST': config('DB_HOST'),
#         'PORT': config('DB_PORT'),
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tour_kg',
        'USER': 'tour_user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5433',
    }
}


AUTH_USER_MODEL = 'user.MyUser'
# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# django-allauth
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_USERNAME_REQUIRED = True  # Требовать имя пользователя
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"  # Обязательное подтверждение email
ACCOUNT_CONFIRM_EMAIL_ON_GET = True  # Подтверждение через GET запрос (ссылка на email)

LOGIN_URL = "/admin"
# Django SMTP
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")  # Ваш email
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")  # Пароль от приложения

REST_AUTH = {
    'USE_JWT': True,  # Включить использование JWT
    'JWT_AUTH_COOKIE': 'auth_token',  # Имя Cookie для хранения Access Token
    'JWT_AUTH_REFRESH_COOKIE': 'refresh_token',  # Имя Cookie для хранения Refresh Token
    'JWT_AUTH_HTTPONLY': True,  # Cookie только для чтения на стороне сервера
    "REGISTER_SERIALIZER": "user.serializers.CustomRegisterSerializer",
}

# Настройка срока действия Access Token и Refresh Token
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # Продолжительность жизни Access Token
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),  # Продолжительность жизни Refresh Token при его использовании
    'SLIDING_TOKEN_LIFETIME': timedelta(days=7),  # Продолжительность жизни Refresh Token
    'SLIDING_TOKEN_REFRESH_REUSE_ALLOWS_REFRESH': False,  # Разрешить повторное использование Refresh Token для обновления
    'SLIDING_TOKEN_REFRESH_REUSE_RESETS': True,  # Сбрасывать Refresh Token после успешного обновления
    'ROTATE_REFRESH_TOKENS': False,  # Вращать Refresh Token (если True, предыдущий Refresh Token становится недействительным после обновления)
    'ALGORITHM': 'HS256',  # Алгоритм подписи токенов
    'AUTH_HEADER_TYPES': ('Bearer',),  # Тип HTTP заголовка, содержащего токен (обычно 'Bearer')
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

# Применение настроек в DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',  # Использование Cookie для хранения JWT
    ],

    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}



# Другие настройки...

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

