import os
from pathlib import Path
from decouple import config
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-key-only-change-in-prod-12345!@#$%')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*', cast=lambda v: [s.strip() for s in v.split(',')])

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
    'channels',
    'drf_spectacular',
    'rides',
    'authentication',
    'notifications',
    'core',
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

CHANNEL_LAYERS = {
    "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}
}

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '5/minute',
        'user': '60/minute',
    }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'SIGNING_KEY': SECRET_KEY,
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Mobile Backend API',
    'DESCRIPTION': 'Production Ready Ride Sharing Backend - Final Audit',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# LOGGING - Task 3 FIXED
LOGS_DIR = BASE_DIR / 'logs'
os.makedirs(LOGS_DIR, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'sensitive_filter': {
            '()': 'core.filters.SensitiveDataFilter',
        },
    },
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'auth_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': str(LOGS_DIR / 'auth.log'),
            'formatter': 'verbose',
            'filters': ['sensitive_filter'],
        },
        'api_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': str(LOGS_DIR / 'api.log'),
            'formatter': 'verbose',
            'filters': ['sensitive_filter'],
        },
        'ride_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': str(LOGS_DIR / 'ride.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'auth': {
            'handlers': ['auth_file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'api': {
            'handlers': ['api_file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'ride': {
            'handlers': ['ride_file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'rides': {
            'handlers': ['ride_file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL', default=False, cast=bool)
CORS_ALLOWED_ORIGINS = config('CORS_ORIGINS', default='http://localhost:3000', cast=lambda v: [s.strip() for s in v.split(',')])
# ============ CELERY CONFIGURATION ============
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_TASK_SOFT_TIME_LIMIT = 20 * 60

# Task Queues - Task 3
from kombu import Queue
CELERY_TASK_QUEUES = (
    Queue('default', routing_key='default'),
    Queue('notifications', routing_key='notifications'),
    Queue('reports', routing_key='reports'),
    Queue('maintenance', routing_key='maintenance'),
)

CELERY_TASK_ROUTES = {
    'rides.tasks.py.send_ride_notification': {'queue': 'notifications'},
    'notifications.tasks.py.send_notification': {'queue': 'notifications'},
    'rides.tasks.py.generate_ride_report': {'queue': 'reports'},
    'rides.tasks.py.generate_daily_summary': {'queue': 'reports'},
    'rides.tasks.py.cleanup_expired_data': {'queue': 'maintenance'},
    'rides.tasks.py.process_background_records': {'queue': 'maintenance'},
}

# Scheduled Jobs - Task 6
from celery.schedules import crontab
CELERY_BEAT_SCHEDULE = {
    'cleanup-expired-every-hour': {
        'task': 'rides.tasks.cleanup_expired_data',
        'schedule': crontab(minute=0, hour='*'),
    },
    'daily-ride-summary-2am': {
        'task': 'rides.tasks.generate_daily_summary',
        'schedule': crontab(minute=0, hour=2),
    },
    'clean-temp-data-midnight': {
        'task': 'rides.tasks.clean_old_temp_data',
        'schedule': crontab(minute=0, hour=0),
    },
}

# Update Throttle - Task 5 from previous story
REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'].update({
    'login': '5/minute',
    'sensitive': '10/minute',
    'burst': '20/minute',
})
def test_report(self):
    r=generate_ride_report.delay("2026-09-09")
    self.assertIn("total_rides",r.get())

def test_cleanup(self):
    r=cleanup_expired_data.delay()
    self.assertIn("Cleaned",r.get())

def test_summary(self):
    r=generate_daily_summary.delay()
    self.assertIn("rides",r.get())
    # For testing without Redis (EPIC 05 Task 8)
    # CELERY_TASK_ALWAYS_EAGER = True  # uncomment for eager testing
    # CELERY_TASK_EAGER_PROPAGATES = True
    CELERY_TASK_DEFAULT_QUEUE = 'default'
    CELERY_TASK_ALWAYS_EAGER = False
    CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
    CELERY_WORKER_HIJACK_ROOT_LOGGER = False



