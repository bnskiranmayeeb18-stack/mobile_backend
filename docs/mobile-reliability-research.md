# Mobile Reliability Research

## Objective
Design APIs that remain reliable when mobile devices have slow networks, retries, duplicate requests, or temporary disconnections.

## 1. Study mobile retry scenarios
Mobile clients face:
- Timeout retries: Request hits server, response lost -> client retries POST
- Offline queue: App queues requests, replays when online
- App kill / rotation: User retries same action manually
- Duplicate tap: Double click on "Book Ride"
- Interceptor trap: Axios retry interceptor generates new Idempotency-Key per attempt (BAD)

## 2. POST operations needing idempotency
- POST /api/rides/create/ -> Ride creation (critical, charge involved)
- POST /api/rides/{id}/accept/ -> Driver accept
- POST /api/rides/{id}/start/ 
- POST /api/rides/{id}/complete/
- POST /api/rides/{id}/cancel/
All state-changing POSTs must be idempotent.

## 3. Idempotency key storage design
Model: IdempotencyKey
- key: UUIDv4 from client header `Idempotency-Key` / `X-Idempotency-Key`
- user_id: scoped per user (key+user unique)
- method + path + body_hash: fingerprint to detect misuse
- response_code + response_body: cached original response
- created_at, expires_at (24h TTL)
- status: processing | completed

Storage: Same DB as business data to keep atomicity. Use unique constraint on (user_id, key) + SELECT FOR UPDATE / get_or_create with savepoint.

Flow:
1. Client generates key once per intent (crypto.randomUUID)
2. Server: INSERT key IF NOT EXISTS -> if exists return cached response
3. Process business logic
4. UPDATE with response
5. On duplicate with different body -> 422

## 4. Duplicate-request protection
- Middleware/decorator checks header
- Fingerprint: sha256(method: path: body)
- Race protection via transaction.atomic + IntegrityError handling
- In-progress 409 Conflict if second request arrives while first processing
- Expiry cleanup via management command / TTL

## 5. Pagination strategy
Offset pagination: simple but unstable under inserts, slow O(offset)
Cursor pagination: stable, fast O(log n), ideal for mobile feeds

We implement:
- CursorPagination with ordering = (-updated_at, -id) composite to break ties
- For sync: `updated_since` + cursor
- Limit default 20, max 100

## 6. updated_at / version fields
Ride model:
- updated_at: auto_now, indexed, for incremental sync
- version: IntegerField for optimistic locking, client sends If-Match
- created_at for ordering

## 7. Incremental sync response design
GET /api/rides/sync/?updated_since=2026-10-14T10:00:00Z&cursor=abc&limit=20
Response:
{
  "items": [rides where updated_at > since],
  "next_cursor": "base64(updated_at:id)",
  "has_more": true,
  "sync_token": "2026-10-15T12:00:00Z"
}

Client stores sync_token, next time asks only delta.

## 8. Simulated failures
Test with:
- Repeat POST with same key -> should return same ride, count ==1
- Different body same key -> 400/422
- Concurrent requests with same key
- Network loss simulation: process completes but client retries

## 9. Client retry rules
- Only retry on network error, timeout, 5xx, 409
- NEVER retry on 4xx (400,401,403,422)
- Use exponential backoff: 1s,2s,4s + jitter, max 3 retries
- Keep same Idempotency-Key across retries
- Generate key per user action, not per HTTP attempt
- Store key in local storage until success acknowledged
- For sync: use updated_since + cursor, handle has_more loop
- Idempotency-Key: UUIDv4 in header `Idempotency-Key: <uuid>`

' + "`" + @'
