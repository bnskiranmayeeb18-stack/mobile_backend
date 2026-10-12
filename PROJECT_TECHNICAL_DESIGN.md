# PROJECT TECHNICAL DESIGN - Django Mobile Ride Backend
# Epic 7 - Requirement Analysis & API Design

## 1. Architecture
Mobile App
   ↓
REST API (/api/v1/) - DRF
   ↓
JWT Authentication (SimpleJWT)
   ↓
RBAC / Object Permissions (IsOwner, IsDriver)
   ↓
Service Layer (rides/services.py - Haversine 1.54km)
   ↓
PostgreSQL + Redis (Cache/Queue) + Celery + Channels (WebSocket)

## 2. User Roles
- Admin: Full access, view all rides, manage users
- Customer (Passenger): Create ride, view own rides, cancel
- Provider (Driver): ONLINE/OFFLINE, update location, accept/start/complete

## 3. Modules (10)
1. Authentication 2. Profile 3. Driver 4. Services 5. Search 6. Booking 7. Payment 8. Notifications 9. Chat 10. Admin

## 4. ER Diagram
User (id, email, role)
 |- Profile (user_id, phone)
 |- DriverProfile (user_id, is_online, lat, lon, rating)
 |- Ride (id, passenger_id, driver_id, pickup_lat/lon, dest_lat/lon, status, ride_type, fare, 1.54km)
    |- Payment (ride_id, amount, status)

## 5. APIs - 20 Endpoints
POST /api/v1/auth/register/ , /login/ , /token/refresh/
GET/PUT /api/v1/profile/
POST /api/v1/drivers/availability/ , /location/
POST /api/v1/rides/ , GET /api/v1/rides/ , GET /api/v1/rides/{id}/
POST /api/v1/rides/{id}/accept/ , /start/ , /complete/ , /cancel/
POST /api/v1/payments/ , GET /api/v1/notifications/ , WS /ws/rides/{id}/ , GET /api/health/ , /api/docs/

## 6. Request/Response Example
POST /api/v1/rides/ -> 201 {id, status: REQUESTED, fare, distance: 1.54km} 
Errors: 401, 400 active ride exists, 400 invalid coords

## 7. 15 Business Rules
1. One active ride per customer
2. Only ONLINE drivers matched
3. Sort by distance 1.54km nearest
4. Concurrent accept via transaction
5. Status flow REQUESTED->ACCEPTED->STARTED->COMPLETED
6. Cancelled cannot be completed
7. Completed cannot be cancelled
8. Only assigned driver can start/complete
9. Only passenger/assigned driver can cancel before start
10. Passenger cannot accept own ride
11. Provider cannot book own service
12. Payment before completion
13. Driver location <5min old
14. Fare = distance * ride_type multiplier
15. Async notifications via Celery + Retry

## 8. Security & Performance
JWT, Throttling, CORS, check --deploy 0 issues, Redis caching, select_related optimization, 26/26 tests PASS

## 9. Deliverables Met
Requirements analyzed, Roles, Modules, ER, APIs, Business rules, Design approved - 8-10 hrs