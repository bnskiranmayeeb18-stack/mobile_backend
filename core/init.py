from .health import health, health_db, health_redis

# old names compatibility
health_check = health
health_database = health_db
health_redis = health_redis
health_celery = health_redis  # celery health same as redis for now