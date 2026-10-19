
### **4. `media_upload/docs/api_contract.md`**
```markdown
# API / Event Contract - Day 1

## REST APIs

### POST /api/media/init/
Request:
{
  "file_name": "photo.jpg",
  "file_size": 5242880,
  "file_type": "image/jpeg",
  "idempotency_key": "client-uuid-123"
}
Response 201:
{
  "upload_id": "uuid",
  "state": "SELECTED",
  "correlation_id": "uuid"
}

### POST /api/media/complete/
Request: { "upload_id": "uuid" }
Response: { "state": "UPLOADED" }

## Events (Server -> Client via Webhook/Polling)
- media.processing: { "upload_id": "...", "correlation_id": "..." }
- media.processed: { "upload_id": "...", "result_url": "..." }
- media.failed: { "upload_id": "...", "reason": "..." }

## Validation Rules
- file_type allowed: image/jpeg, image/png, video/mp4
- file_size max: 100MB