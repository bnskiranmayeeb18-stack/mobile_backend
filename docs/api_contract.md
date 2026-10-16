# API Contract

POST /api/media/upload/
- Auth: Bearer Token
- Body: multipart file, idempotency_key (optional)
- Success 201: {id, status: PENDING, correlation_id}
- Errors: 400 invalid file, 413 oversized, 401/403 auth

GET /api/media/{id}/status/
- Returns: {id, processing_status, error_message?, correlation_id}
- Mobile polls this

GET /api/media/{id}/
- Returns file or presigned URL
- 403 if not owner

Error Format (consistent):
{ "error": { "code": 400, "message": "...", "correlation_id": "uuid" } }

Logs: structured JSON with correlation_id, media_id, user_id, event