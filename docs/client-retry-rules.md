# Client Retry Rules
- Retryable: network error, timeout, 5xx, 429
- Non-retryable: 4xx except 408,429
- Backoff: 1s,2s,4s + jitter
- Max retries: 3
- Use Idempotency-Key uuid v4 for all POST/PATCH
- Offline queue: local DB, sync on reconnect via /sync/
- On 409 conflict: fetch latest, merge, retry
