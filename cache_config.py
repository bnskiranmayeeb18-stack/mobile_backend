# mobile_backend/settings.py ki add chey

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'mobile-backend-cache',
    }
    # Production: 
    # 'default': {
    #     'BACKEND': 'django_redis.cache.RedisCache',
    #     'LOCATION': 'redis://127.0.0.1:6379/1',
    # }
}

# For production validation - simple cache check
