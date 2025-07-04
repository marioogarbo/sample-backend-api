import os
import sys
import dj_database_url

from pathlib import Path
from dotenv import load_dotenv


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Load environment variables from a .env file
load_dotenv(override=True)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

if not SECRET_KEY:
    raise ValueError('The DJANGO_SECRET_KEY environment variable is not set.')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() == 'true'

DEVELOPMENT_MODE = os.getenv('DEVELOPMENT_MODE', 'False').lower() == 'true'

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework_simplejwt',
    'rest_framework',
    'corsheaders',
    'social_django',
    'storages',
    'djoser',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

if DEVELOPMENT_MODE is True:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
elif len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
    if os.getenv('DATABASE_URL', None) is None:
        raise Exception('DATABASE_URL environment variable not defined')
    DATABASES = {
        'default': dj_database_url.parse(os.getenv('DATABASE_URL')),
    }


# Custom user model
AUTH_USER_MODEL = 'users.UserAccount'


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

if DEVELOPMENT_MODE is True:
    STATIC_URL = 'static/'
    STATIC_ROOT = BASE_DIR / 'static'
    MEDIA_URL = 'media/'
    MEDIA_ROOT = BASE_DIR / 'media'
else:
    STORAGES = {
        'default': {
            'BACKEND': 'storages.backends.s3.S3Storage',
            'OPTIONS': {
                'secret_key': os.getenv('AWS_S3_SECRET_ACCESS_KEY'),
                'access_key': os.getenv('AWS_S3_ACCESS_KEY_ID'),
                'bucket_name': os.getenv('AWS_S3_BUCKET_NAME'),
                'region_name': os.getenv('AWS_S3_REGION_NAME'),
                'endpoint_url': 'https://{region_name}.digitaloceanspaces.com',
                'object_parameters': {'CacheControl': 'max-age=86400'},
                'default_acl': 'public-read',
                'location': 'static',
                'custom_domain': os.getenv('AWS_S3_CUSTOM_DOMAIN'),
            },
        },
        'staticfiles': {
            'OPTIONS': {
                'secret_key': os.getenv('AWS_S3_SECRET_ACCESS_KEY'),
                'access_key': os.getenv('AWS_S3_ACCESS_KEY_ID'),
                'bucket_name': os.getenv('AWS_S3_BUCKET_NAME'),
                'region_name': os.getenv('AWS_S3_REGION_NAME'),
                'endpoint_url': 'https://{region_name}.digitaloceanspaces.com'
            },
        },
    }


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# DJOSER settings
DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': os.getenv('PASSWORD_RESET_CONFIRM_URL'),
    'SEND_ACTIVATION_EMAIL': True,
    'ACTIVATION_URL': os.getenv('ACTIVATION_URL'),
    'USER_CREATE_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'TOKEN_MODEL': None,
    'SOCIAL_AUTH_ALLOWED_REDIRECT_URIS': os.getenv('REDIRECT_URLS').split(','),
    'EMAIL_FRONTEND_DOMAIN': os.getenv('EMAIL_FRONTEND_DOMAIN'),
    'EMAIL_FRONTEND_SITE_NAME': os.getenv('EMAIL_FRONTEND_SITE_NAME'),
}

if not DJOSER['PASSWORD_RESET_CONFIRM_URL']:
    raise ValueError("PASSWORD_RESET_CONFIRM_URL environment variable is not set. \
                     Please set it to the URL for password reset confirmation.")


# REST framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'users.authentication.CustomJWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}


# CORS settings
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS= False
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS').split(',')
CSRF_TRUSTED_ORIGINS= os.getenv('CORS_ALLOWED_ORIGINS').split(',')

if not CORS_ALLOWED_ORIGINS:
    raise ValueError("CORS_ALLOWED_ORIGINS environment variable is not set or empty. \
                     Please set it to a comma-separated list of allowed origins.")


# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'webmaster@localhost')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True')
EMAIL_PORT = os.getenv('EMAIL_PORT', '587')

if not EMAIL_HOST or not EMAIL_HOST_USER or not EMAIL_HOST_PASSWORD:
    raise ValueError("Email settings are not properly configured. \
                     Please set EMAIL_HOST, EMAIL_HOST_USER, and EMAIL_HOST_PASSWORD \
                     in your environment variables.")