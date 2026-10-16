# Mobile Backend - Reliable Media Pipeline

> 5-Day Track (12-16 Oct 2026) - Secure, Observable, Resilient Media Uploads

## 🎯 Objective
Make media uploads reliable, secure, observable, integrated with mobile events.

## 📁 Architecture

`Upload -> Validate -> Secure Storage -> Async Processing (Celery) -> Retrieval`

- **Storage Naming**: `{user_id}/{uuid}_{original_filename}` - no collisions
- **Status Flow**: PENDING -> PROCESSING -> READY / FAILED
- **Events**: `processing-started`, `processing-completed`, `processing-failed` with `correlation_id`

## 🔒 Security & Reliability

- Auth + ownership check - 403 if not owner
- File type whitelist: jpeg/png/mp4 - 10MB/100MB limits
- Invalid/oversized -> `400` with `{error: {code, message, correlation_id}}`
- Idempotent: `select_for_update()` + idempotency_key - retries don't duplicate
- Retries: 3x backoff, no duplicate side-effects

## 📊 Observability

- Structured logs: `correlation_id`, `media_id`, `user_id`, `event`
- Status endpoint: `GET /api/media/{id}/status/`
- Mobile polls status, reflects accurately

## 🚀 Setup

```bash
pip install -r requirements.txt
python manage.py migrate
celery -A core worker -l info
python manage.py runserver