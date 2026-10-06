# EPIC 04 - Task 1 - Review Existing Project - Problems Found - 31-Aug-2026
# Project: bnskiranmayee18-stack/mobile_backend
# Trainee: Kiranmayee

## Reviewed Areas: 9/9

### 1. Permissions
**Found:**
- IsAuthenticated used but IsOwner not consistently applied on all ride/vehicle APIs
- Permission classes duplicated in views, not centralized
- Object-level permission check missing in some ViewSets
**Problem:** Security risk - user can access other's data if IsOwner missing

### 2. Celery tasks
**Found:**
- tasks.py has business logic + notification logic tightly coupled
- No retry logic for failed tasks (max_retries missing earlier)
- No idempotency_key check inside task - duplicate notifications possible
- Broker URL hardcoded, not from settings
**Problem:** Reliability, duplicate execution

### 3. WebSocket consumers
**Found:**
- JWT authentication parsing inside consumer - should be in middleware/service
- Business logic (ride status update) inside consumer, not service layer
- No centralized disconnect handling
- Group name hardcoded ride_{id}
**Problem:** Consumer is fat, tightly coupled

### 4. Models
**Found:**
- Some FK missing db_index=True (driver_id, user_id check needed)
- No unique_together / UniqueConstraint on critical fields earlier fixed
- __str__ methods missing for some models
- No custom Manager for common queries
**Problem:** Performance, data integrity

### 5. Serializers
**Found:**
- Validation logic duplicated across serializers
- Nested serializers causing N+1
- No separation of read/write serializers
**Problem:** Maintainability, performance

### 6. Views
**Found:**
- Views contain business logic - fare calculation, cache logic inside views
- Fat views, thin services - opposite needed for production
- cache logic directly in views instead of service layer
- No consistent response format
**Problem:** Main EPIC 04 issue - business logic tightly coupled to API views

### 7. URLs
**Found:**
- URLs include all routes in single file? Check include pattern
- No versioning /api/v1/
- Swagger not added for all endpoints
**Problem:** Scalability

### 8. Services
**Found:**
- cache_service.py exists but ride_service.py, driver_service.py missing
- Business logic scattered - no dedicated service layer
- No interface / abstraction
**Problem:** Need to create clean service layer - EPIC 04 objective

### 9. Utilities
**Found:**
- No utils/ folder - helper functions inside views
- Rate limiting logic duplicated
- Common functions like idempotency generation duplicated
**Problem:** Code reuse missing

---
## SUMMARY - Problems Found: 15+

1. Business logic tightly coupled to views - Needs service layer extraction
2. Fat views, thin services - Reverse needed
3. Permissions not centralized
4. Celery tasks not idempotent
5. WebSocket consumers contain business logic
6. N+1 still possible without service layer
7. No API versioning
8. Missing centralized utils
9. No repository pattern
10. Hardcoded Redis/Celery URLs
11. No observability / logging centralization

## NEXT: Task 2 - Identify Responsibilities
For every main API, identify responsibilities to move to service layer.