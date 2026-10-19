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
 
---
## Day 2 - 20 Oct 2026 - Reliable Transfer - Tuesday

**Story:** Reliable transfer and retry
**Objective:** Complete engineering outcome and commit working changes
**Practical:** Interrupted transfer can resume or fail safely without corrupting final state

**Tasks Done:**
- Safe retry via Idempotency-Key header
- Size/type validation 2MB
- Bounded retries FAILED->STAGING

**Implementation:**
- views.py: Idempotency check FIRST, then validation, then create
- Returns 200 Duplicate with same ID - no corruption
- MAX_SIZE 2MB, ALLOWED image/*

**Acceptance Criteria Met:**
1. Versioned: commit 389af10 pushed to main
2. Evidence: 201 PENDING + 200 Duplicate + correlation_id + 400 negative
3. README: Decisions, steps, limitations documented

**Proofs:**
- 201 id: 5b892c7d-bfc4-4972-ae48-bd67b3c6da69
- 200 Duplicate id: 5b892c7d... (29ms) & 196e8bfc... (9ms) - SAFE RETRY
- 
- correlation_id: eba83113..., ca8e7a41...

**Known Limitations:**
- No chunk/resume (single file POST)
- In-memory idempotency, would use Redis in prod
- 2MB hardcoded

**Status: ALL PASS
# Mobile Backend - Media Processing

## Day 3 - Idempotent Event Processing ✅ COMPLETE

### Overview
Handles duplicate and out-of-order webhook events without creating duplicate results.

### Architecture
- **Media** model: Stores uploaded media status
- **ProcessedEvent** model: Event ledger with UNIQUE(event_id)
    - Prevents duplicate processing at DB level
    - Tracks media_id, event_type, result, correlation_id

### Idempotency Logic (media_upload/views.py)

1. **Duplicate Detection (Fast Path)**
   ```python
   PROCESSED_EVENTS = {} # in-memory
   if event_id in PROCESSED_EVENTS: return 200 Duplicate
