# API Design - Saved Services

## Endpoints
POST   /api/v1/saved-services/
GET    /api/v1/saved-services/
DELETE /api/v1/saved-services/{id}/

## POST - Save
Auth: JWT IsAuthenticated + IsCustomer
Req: {"service_id": "uuid"}
Res 201: {"id":"...","customer":1,"service":{...},"created_at":"..."}
Res 200: already saved - idempotent return existing
Errors: 401, 400 invalid uuid, 404 service not found

## GET - List
Auth: JWT
Query: ?page=1&page_size=20
Res 200: {"count":50,"next":"...","results":[{"id":...,"service":{...}}]}
Uses select_related('service','customer'), pagination 20, cache 60s
Filtered by request.user -> prevents IDOR

## DELETE - Remove
Auth: JWT Owner only
Res 204 No Content
Errors: 401, 404 (not found or not owned - prevents enumeration)

## Permissions
IsAuthenticated + IsCustomer + IsOwner (queryset filter by user)

## Performance
select_related, db_index on customer/service/created_at, composite unique (customer,service), pagination, cache key saved_services_user_{id}_page_{n} TTL 60s
