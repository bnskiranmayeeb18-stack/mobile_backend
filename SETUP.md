# Setup Guide

1. pip install -r requirements.txt
2. Add to settings: CELERY_BROKER_URL, MEDIA_STORAGE, LOGGING with correlation_id filter
3. python manage.py migrate
4. celery -A core worker -l info
5. python manage.py runserver

Tests:
python manage.py test media_app.tests.test_reliability -v2
python manage.py test media_app.tests.test_integration -v2

Env: AWS keys, MAX_UPLOAD_SIZE