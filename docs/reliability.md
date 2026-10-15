# Mobile Reliability Design

## Problem
Mobile network lo: slow network, user double-tap, auto-retry, disconnection valla same POST 2-3 sarlu vastundi -> duplicate rides.

## Solution
1. **Idempotency-Key Header**: Client prati POST ki UUID v4 pampali `Idempotency-Key: <uuid>`
   - Server same key + user + path ki same response istundi 24h varaku
   - Storage: core_idempotencykey table (key, user, path, request_hash, response)

2. **Ride-level idempotency**: `rides_ride.idempotency_key` unique per user
   - Second request with same key -> existing ride return, new create kadu

3. **Versioning / Optimistic Locking**:
   - `version` field increment on every update
   - Client update chesetappudu `If-Match: version` pampali, mismatch ayithe 409 Conflict

4. **Sync-Friendly Endpoints**:
   - Pagination: `?limit=20&offset=0`
   - Incremental Sync: `GET /rides/?updated_after=2026-10-15T10:00:00Z`
   - Ordering: `-updated_at, -id` (cursor stable)

5. **Client Retry Rules**:
   - POST: Always send Idempotency-Key, retry on 408, 429, 5xx, network timeout with exponential backoff (1s, 2s, 4s). Never retry without same key.
   - GET: Safe to retry infinitely.
   - On 409: Fetch latest, merge, retry with new version.
   - On 201 with same key: Treat as success (duplicate protection working).

## Tests
pytest tests/test_task4_ride_api.py -> idempotent create
pytest tests/test_task6_database.py -> cascade delete safety
Total 37 passed.