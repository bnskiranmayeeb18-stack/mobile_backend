
New-Item -ItemType Directory -Force -Path docs
@"
# API Design - Saved Services

### POST /api/v1/saved-services/
Auth: Bearer JWT, Permission: IsAuthenticated
Request: {"service_id": "uuid"}
Responses:
- 201: {id, customer, service:{...}, created_at}
- 200: {"message":"Already saved", "data": {...}} (duplicate)
- 400: {"error":"service_id required"} / invalid UUID
- 404: {"error":"Service not found"}
- 401: Unauthorized

### GET /api/v1/saved-services/
Auth: Required, Owner-only via get_queryset()
Cache: Redis key saved_services_user_{id}_page_{page} TTL 60s
Response 200: {count, next, previous, results: [{id, customer, service, created_at}]}

### DELETE /api/v1/saved-services/{id}/
Auth: Required, checks owner in remove_saved_service()
Response: 204 No Content, 404 Not Found

Permissions: All endpoints IsAuthenticated, queryset filtered to request.user
Status Codes: 200,201,204,400,401,404
"@ | Set-Content -Path docs/API_DESIGN.md -Encoding UTF8
# API Design - Saved Services

Base: /api/v1/saved-services/

### POST /api/v1/saved-services/
- Auth: Bearer JWT Required
- Permission: IsAuthenticated
- Request: { "service_name": "plumbing" }
- Response 201: { "id": 1, "user": 5, "service_name": "plumbing", "created_at": "..." }
- Errors: 400 Duplicate, 400 Invalid payload, 401 Unauthorized, 404 Service Not Found

### GET /api/v1/saved-services/
- Auth: JWT
- Permission: Owner only - queryset = SavedService.objects.filter(user=request.user)
- Response 200: [{...}, {...}]
- Errors: 401

### DELETE /api/v1/saved-services/{id}/
- Auth: JWT
- Permission: Owner only
- Response: 204 No Content
- Errors: 401, 404 Not Found

### Status Codes
201 Created, 200 OK, 204 Deleted, 400 Bad Request, 401 Unauthorized, 404 Not Found

### Security
- IsAuthenticated
- get_queryset filters by request.user -> IDOR blocked
- UniqueConstraint(user, service_name)