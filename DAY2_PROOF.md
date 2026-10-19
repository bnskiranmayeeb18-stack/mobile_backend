# Day 2 - Reliable Transfer - ALL PASS - 19-10-2026

## Postman Proofs (Screenshots)
1. 201 Created - PENDING - id: 5b892c7d-bfc4-4972-ae48-bd67b3c6da69 - 434ms - PASS
2. 200 OK - COMPLETED Duplicate - same id 5b892c7d... - 29ms - SAFE RETRY PROOF - PASS
3. 201 Created - PENDING - id: 5c4999e2-a94a-4d64-8c9c-b027cd9289b4 - correlation_id ca8e7a41... - 83ms - PASS
4. 200 OK - COMPLETED Duplicate - id: 196e8bfc-dc69-4f48-85c2-fd5e2abd0637 - 9ms - PASS

## Implementation Verified
- Idempotency-Key header mandatory, case-insensitive check
- Existing key -> returns 200 with same ID, detail: Duplicate - idempotent return
- No duplicate rows, no corruption on retry - bounded retries working
- Correlation ID for tracing: fe0ed38d..., ca8e7a41..., eba83113...
- State transitions: SELECTED -> STAGING -> UPLOADING -> UPLOADED (legal)
- Size validation: 2MB max added in views.py - returns 400 File too large
- Type validation: image/* only - returns 400 Invalid type
- Django 6.1.1, System check 0 issues, WSGI dev server at 127.0.0.1:8000

## Task 8 Requirement
"Interrupted transfer resumes without corrupting final state, server checks file size/type, correlation ID"
-> ALL SATISFIED

## Server
October 19, 2026 - 12:22:23 - Watching for file changes with StatReloader
