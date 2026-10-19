# REQUIREMENT.md - Saved Services - 02-Oct-2026
## Problem
Customers need to bookmark services for later. No save feature currently.

## Users
- Customer: save/view/remove + get notification on availability change
- Provider: availability change triggers notifications
- System: Celery background notification

## Functional
1. POST /api/v1/saved-services/ - save service
2. GET /api/v1/saved-services/ - list with pagination
3. DELETE /api/v1/saved-services/{id}/ - remove
4. Notification when saved service availability changes
5. No duplicate saves
6. Owner-only access
7. # Saved Services - Requirement Analysis

## Problem
Customers browse many services but lose track. Need wishlist to save & get notified when availability changes.

## Users
- Customer (Authenticated)
- Admin (Service availability update)

## Functional Requirements
1. Customer can save a service
2. Customer can list saved services
3. Customer can remove saved service
4. System sends notification when saved service availability changes
5. Duplicate save not allowed

## Non-Functional Requirements
- Auth: JWT Bearer Token
- Performance: Cached list view (Redis), <200ms
- Security: IsOwner permission, no other user data leak
- Scalability: Celery async notification

## Business Rules
- Only available services can be listed? No, can save unavailable also but notify
- One customer + one service = unique
- Soft delete not needed, hard delete on unsave

## Edge Cases
- Service deleted -> SavedService CASCADE
- Duplicate save -> 400 Bad Request
- Invalid UUID -> 404
- Unauthorized -> 401
- Service becomes unavailable -> Celery task trigger
- Cache stale -> delete_pattern / clear

## Non-Functional
- <200ms list (cached)
- Pagination 20, 1000+ per user
- Idempotent save
- Notification <5s via Celery
- No IDOR, auth required

## Business Rules
- Only active services can be saved
- Unique (customer, service)
- Availability change -> notify all savers
- Saved remains even if unavailable
- Only customers can save

## Edge Cases
- Service deleted -> cascade delete saved
- Duplicate save -> return 200 with existing (idempotent)
- Service not found -> 404
- Unauthorized -> 401, other's id -> 404 not 403
- Rapid toggle -> debounce 5min
- Empty list -> [] 200 not 404
- Customer delete -> cascade
- @"
# Saved Services Feature - Requirement Analysis

## Problem
Customers need ability to bookmark services for quick access. No way to track favorite services currently.

## Users
- Customer (Authenticated User): Can save, view, remove services
- Admin: Manage services availability

## Functional Requirements
1. FR1: Customer can save a service via service_id
2. FR2: Customer can view paginated list of saved services
3. FR3: Customer can remove saved service
4. FR4: System sends notification when saved service availability changes
5. FR5: Duplicate save returns 200 with message "Already saved"

## Non-Functional Requirements
- NFR1: Response time < 200ms (use Redis caching 60s per page)
- NFR2: Secure - JWT auth required
- NFR3: Scalable - pagination, indexed queries
- NFR4: Background processing via Celery

## Business Rules
- BR1: One customer can save a service only once (UniqueConstraint customer+service)
- BR2: Only authenticated customers can access own saved services
- BR3: service_id must be valid UUID of existing Service
- BR4: Cache invalidation on create/delete

## Edge Cases
- Service does not exist -> 404
- service_id missing -> 400
- Invalid UUID format -> 400
- Duplicate save -> 200 Already saved
- Unauthorized -> 401
- Deleting other user's saved service -> 404
- Service becomes unavailable -> trigger Celery notification
"@ | Set-Content -Path REQUIREMENT.md -Encoding UTF8
- # Saved Services Feature - Requirement Analysis
Date: 02-Oct-2026

## Problem
Customers browse many services but have no way to bookmark/favorite for later. They miss when availability/price changes.

## Users
- Customer: Save, List, Remove services
- System: Detect availability change -> notify
- Admin: View saved counts

## Functional Requirements
1. FR1: Customer can save a service (POST /api/v1/saved-services/)
2. FR2: Customer can view own saved services list (GET)
3. FR3: Customer can remove saved service (DELETE /{id}/)
4. FR4: Prevent duplicate saves (same user + service_name unique)
5. FR5: When saved service becomes unavailable, send notification via Celery task
6. FR6: Only owner can access his saved list (IDOR prevention)

## Non-Functional Requirements
- Auth: JWT required, IsAuthenticated
- Performance: Query optimized with select_related, index on (user, service_name)
- Security: IDOR blocked, no anon access 401
- Scalability: Celery + Redis for async notifications
- Data Integrity: Unique constraint

## Business Rules
- BR1: One user cannot save same service_name twice -> 400
- BR2: SavedService.user = request.user only
- BR3: Notification sent only if service availability = False
- BR4: Soft delete not required, hard DELETE = 204

## Edge Cases
- EC1: Service ID 99999 -> 404 Service Not Found
- EC2: Unauthenticated -> 401
- EC3: Delete other user's saved id -> 404 (not 403, to avoid enumeration)
- EC4: Long service_name >255 -> 400
- EC5: Empty payload -> 400
- EC6: Concurrent duplicate saves -> only one succeeds (DB unique constraint)
@"
## Day 2 - 20 Oct 2026 - Reliable Transfer

**Objective:** Interrupted transfer resume without corrupting final state

**Decision:** Safe retry via Idempotency-Key (sample workflow supports idempotent POST, not chunked). No duplicate rows, return same ID with 200 Duplicate.

**Execution:**
1. python manage.py runserver 8000
2. POST /api/media/upload/ with Idempotency-Key header
3. Retry same key -> 200 Duplicate, same ID, 9-29ms (proves no corruption)
4. Size test 3MB -> 400, Type test txt -> 400

**Proofs:** 201 (id: 5b892c7d...), 200 Duplicate (id: 5b892c7d... & 196e8bfc...), correlation_id tracing

**Known Limitations:**
- No chunk/resume (single file POST), bounded retries via FAILED->STAGING allowed
- In-memory idempotency map, not persistent DB (would use Redis in prod)
- 2MB limit hardcoded, not configurable


