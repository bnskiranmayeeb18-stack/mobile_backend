import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-your-secret-key-change-in-prod-12345'

DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'core',
    'rides',
    'notifications',
]
MIDDLEWARE = [
    'core.middleware.request_id.RequestIDMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mobile_backend.urls'

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

WSGI_APPLICATION = 'mobile_backend.wsgi.application'
ASGI_APPLICATION = 'mobile_backend.asgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS
CORS_ALLOW_ALL_ORIGINS = True

# Cache - Redis with fallback to LocMem
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Try Redis if available
try:
    import django_redis
    CACHES['default'] = {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
except:
    pass

# Auth User
AUTH_USER_MODEL = 'accounts.User' if 'accounts' in INSTALLED_APPS else 'auth.User'

# ================= OBSERVABILITY - EPIC 10-SEP =================
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'structured': {
            'format': '[{asctime}] [{levelname}] [{name}] {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'structured',
        },
        'file_app': {
            'class': 'logging.FileHandler',
            'filename': str(LOG_DIR / 'application.log'),
            'formatter': 'structured',
        },
        'file_api': {
            'class': 'logging.FileHandler',
            'filename': str(LOG_DIR / 'api.log'),
            'formatter': 'structured',
        },
    },
    'loggers': {
        'application': {'handlers': ['console', 'file_app'], 'level': 'INFO', 'propagate': False},
        'authentication': {'handlers': ['console', 'file_app'], 'level': 'INFO', 'propagate': False},
        'api': {'handlers': ['console', 'file_api'], 'level': 'INFO', 'propagate': False},
        'database': {'handlers': ['console'], 'level': 'WARNING', 'propagate': False},
        'celery': {'handlers': ['console', 'file_app'], 'level': 'INFO', 'propagate': False},
        'websocket': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
        'security': {'handlers': ['console', 'file_app'], 'level': 'WARNING', 'propagate': False},
        'django.db.backends': {'handlers': ['console'], 'level': 'WARNING', 'propagate': False},
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    }
}

# REST Framework
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'core.exceptions.custom_exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'core.throttling.BurstRateThrottle',
        'core.throttling.SustainedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'burst': '20/min',
        'sustained': '100/hour',
        'anon': '10/min',
    }
}

# JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

# Celery
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'