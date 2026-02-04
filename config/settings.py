"""
Django settings for config project - Digital Fortress Edition.
"""

from pathlib import Path
import os
import sys
import environ  # pip install django-environ
from datetime import timedelta

# 1. Környezeti változók inicializálása
env = environ.Env(
    # Default értékek, ha nincs .env fájl (fejlesztéshez)
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Olvassa be a .env fájlt a gyökérkönyvtárból
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Az 'apps' mappa hozzáadása a Python path-hoz
sys.path.append(str(BASE_DIR / 'apps'))


# 2. Biztonsági beállítások
SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')


# 3. Application definition
INSTALLED_APPS = [
    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',  # JWT Auth
    'corsheaders',               # Frontend kommunikációhoz
    'mptt',                      # Hierarchikus kategóriákhoz
    'django_filters',            # Kereséshez

    # Local apps (A te moduljaid)
    'core',
    'catalog',
    'analytics',
    'sales',
    'billing',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS legyen elöl!
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # Saját Middleware-ek
    # 'apps.core.middleware.IdempotencyMiddleware',  # Csak akkor kapcsold be, ha már megírtad a fájlt!
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


# 4. Adatbázis (PostgreSQL)
# A .env fájlban így néz ki: DATABASE_URL=postgres://user:pass@host:port/dbname
DATABASES = {
    'default': env.db(),
}


# 5. Cache & Redis (A/B teszthez és Idempotenciához)
# A .env-ben: REDIS_URL=redis://redis:6379/1
CACHES = {
    'default': env.cache('REDIS_URL', default='locmemcache://'),
}


# 6. User Model (Custom User)
# FONTOS: Ezt az apps/core/models.py-ban létre kell hoznod a migrate előtt!
AUTH_USER_MODEL = 'core.User' 


# 7. Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# 8. Internationalization
LANGUAGE_CODE = 'hu-hu'  # Magyar lokalizáció
TIME_ZONE = 'Europe/Budapest'
USE_I18N = True
USE_TZ = True


# 9. Static & Media files
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'


# 10. Django Rest Framework Config (A "Motor")
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated', # Alapból minden zárt
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    }
}

# 11. JWT Beállítások
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}


# 12. Celery Configuration (Aszinkron feladatok)
CELERY_BROKER_URL = env('REDIS_URL', default='redis://redis:6379/0')
CELERY_RESULT_BACKEND = env('REDIS_URL', default='redis://redis:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'


# 13. Stripe Config
STRIPE_PUBLIC_KEY = env('STRIPE_PUBLIC_KEY', default='')
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY', default='')
STRIPE_WEBHOOK_SECRET = env('STRIPE_WEBHOOK_SECRET', default='')


# 14. CORS (Frontend engedélyezés)
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=['http://localhost:3000'])


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'