# EPIC 02 - Task 1 - Business Logic Identification
Date: 13-Aug-2026

## Objective
Move important business logic away from API views and build reusable, testable service logic.

## Identified Business Logic

### 1. Fare Calculation
- Formula: fare = (distance_km * 15) + (duration_min * 2) + base_fare
- Surge pricing in peak hours
- Location: core/services/fare_service.py
- Reason: Reusable, needs testing, changes frequently

### 2. Ride Eligibility
- User cannot request if: has active ride, unpaid dues, blocked
- Location: core/services/eligibility_service.py

### 3. Driver Assignment Rules
- Driver must be: ONLINE, within 5km, no active ride, rating > 4.0
- Location: core/services/driver_service.py

### 4. Cancellation Rules
- REQUESTED: free cancel
- ACCEPTED: Rs 30 fee
- STARTED: Rs 80 fee
- COMPLETED: cannot cancel -> 400 error
- Location: core/services/cancellation_service.py

### 5. Ride Status Transitions (Implemented in Task 8)
- Valid: REQUESTED -> ACCEPTED -> STARTED -> COMPLETED
- Valid: REQUESTED/ACCEPTED -> CANCELLED
- Invalid: COMPLETED -> ACCEPTED (400 Bad Request) - Proof in task-8-05
- Location: core/models.py (validation) + core/services/ride_service.py

## Decision
No business logic in views.py
Views only: request validation -> call service -> return response
All logic moved to core/services/