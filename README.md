# Mobile Backend - Media Pipeline (12-16 Oct 2026)

## Architecture
Upload -> Validation -> PENDING + correlation_id -> Celery process_media -> COMPLETED/FAILED -> Retrieval

## API
POST /api/media/upload/ [Auth, Idempotency-Key, file]
GET /api/media/{id}/
GET /api/media/

## Security
- Owner-only queryset
- PIL validation, 10MB limit
- Idempotency via IdempotencyRecord
- Private S3 naming: media/{user_id}/{uuid}.jpg

## Observability
Logs: correlation_id in all events
Events: media_upload_started, processing-started, processing-completed

## E2E Verified (15 Oct)
Upload: 201 id=4bf90248-995a-4e50-a5ec-89e61396023c
Task succeeded in 0.058s
Status: COMPLETED Size: 633

## Run Tests
python manage.py test media_app.tests -v 2

## Setup
pip install -r requirements.txt
python manage.py migrate
celery -A mobile_backend worker -l info

## Acceptance: ALL PASS
Decisions: Django + Celery + IdempotencyExecution steps: how to run server, workerLegal states: PENDING, PROCESSING, COMPLETED, FAILEDFailure transitions: invalid file -> FAILEDKnown limitations: file size <2MB
