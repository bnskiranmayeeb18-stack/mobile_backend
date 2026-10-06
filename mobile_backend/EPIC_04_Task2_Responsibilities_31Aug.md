# Task 2 - Identify Responsibilities - 31Aug

# Architecture Flow: Request -> Serializer -> View -> Service -> Repository/ORM -> Database

## 1. Request Layer
- Responsibility: HTTP request vastundi, JWT token, headers
- Example: POST /api/rides/ with Bearer token
- Logic: ZERO - em logic undadu

## 2. Serializer Layer
- Responsibility: Validation ONLY
- Chesedi: input data correct ah kada ani check - lat/lng numbers ah, status valid ah
- Cheyadhu: DB query cheyadhu, fare calculate cheyadhu, cache cheyadhu
- File: rides/serializers.py

## 3. View Layer - THIN ga undali - Ikkade problem undi ippudu
- Responsibility: Permission check + serializer call + service call + response return - ONLY 4 lines
- Chesedi: IsAuthenticated, IsOwner check, serializer.is_valid(), service ki pampadam
- Cheyadhu: Database operation cheyadhu (Ride.objects.filter BAD), business logic cheyadhu (fare calc BAD), cache logic cheyadhu (cache.set BAD)
- Current Problem: Mana views lo 50+ lines unnayi with DB operations - idi Task 3 lo fix cheyali
- File: rides/views.py, drivers/views.py

## 4. Service Layer - MAIN LOGIC IKKADA - Idi kottha ga create cheyali - EPIC 04 goal
- Responsibility: Business logic antha ikkada
- Chesedi:
  RideService.create_ride() -> fare calc, driver assign, cache set, notification trigger
  DriverService.find_nearby() -> Redis lo nearby drivers search, TTL 60s
  VehicleService.create() -> plate unique check, ownership check
  NotificationService.send() -> idempotency_key tho duplicate prevent
- File: services/ride_service.py (kottha create cheyali)
- Idi Task 2 main output

## 5. Repository/ORM Layer
- Responsibility: DB queries optimise chesi ivvadam
- Chesedi: select_related('user','driver') tho N+1 fix, db_index use, cache get/set
- Cheyadhu: business logic cheyadhu
- File: rides/repositories.py or services lo ORM part

## 6. Database Layer
- Responsibility: Data store with indexes
- Indexes: user_id, driver_id, status, plate_number unique
- Constraints: unique_together, idempotency_key unique
- PostgreSQL + Redis

---

## Every Major API ki Responsibility - Table

API: POST /api/rides/ (Ride Create)
- Request: JSON with pickup, drop
- Serializer: Validate pickup/drop present ah
- View: serializer.is_valid() + RideService.create_ride() call + return 201 - ONLY 4 LINES
- Service: calculate_fare() + find driver + cache set driver_{id} + send_notification_async.delay()
- Repository: Ride.objects.create(), Driver.objects.select_related()
- Database: Insert into rides table with indexes

API: GET /api/rides/ (Ride List)
- Serializer: Validate status filter
- View: RideService.get_user_rides(user) call
- Service: Cache check get_ride_cache(), miss ayithe DB nundi, 0.046ms vs 50ms
- Repository: Ride.objects.filter(user_id).select_related() 5 queries -> 1 query
- Database: Index scan on user_id

API: PATCH /api/rides/{id}/ (Status Update)
- View: IsOwner check + RideService.update_status()
- Service: Status validation + cache invalidate + WebSocket group_send ride_{id} broadcast
- Repository: Ride.objects.filter(id).update(status)
- Database: Update with status index

API: GET /api/drivers/nearby/?lat=&lng=
- View: lat/lng get + DriverService.find_nearby(lat,lng)
- Service: Redis available_drivers key 60s TTL, geospatial logic
- Repository: Redis get/set
- Database: Redis

API: WebSocket /ws/ride/{id}/?token=
- Request: token query param
- View/Consumer: Auth check - scope["user"]
- Service: AuthService.verify_token() + RideService.handle_update()
- Repository: channel_layer.group_send()

---

## Conclusion: What belongs to each layer?
- Validation -> Serializer
- Permission + orchestration -> View (THIN)
- Business logic, cache, Celery, WS -> Service (FAT)
- DB queries optimized -> Repository/ORM
- Storage -> Database

Problem: Currently business logic in View - Need to move to Service - This is Task 3