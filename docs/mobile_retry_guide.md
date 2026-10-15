# docs/mobile_retry_guide.md
## Mobile Retry Rules

1. POST operations needing idempotency: /api/rides/create/, /api/rides/<id>/accept/, /api/rides/<id>/update/
2. Client must generate UUID v4 once per logical operation and reuse on retry.
3. Send header: Idempotency-Key: <uuid>
4. Server stores key 24h, replays same response for same payload, 409 for different payload.
5. Pagination: Use cursor?cursor=<updated_at> & limit=20 - stable under inserts.
6. Sync: GET /api/rides/sync/?since=ISO8601 - returns updated_at, version, server_time.
7. On timeout: retry with same key, exponential backoff 1s,2s,4s, max 3 retries.
8. Partial failure: If response unknown, call sync to reconcile.
