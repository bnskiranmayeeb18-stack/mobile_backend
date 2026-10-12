# Mobile Application Backend - Django REST Framework

## Live API
Base URL: https://mobile-backend-2kc1.onrender.com
- Swagger UI: https://mobile-backend-2kc1.onrender.com/swagger/
- Redoc: https://mobile-backend-2kc1.onrender.com/redoc/
- Local Docs: http://127.0.0.1:8000/api/docs/

## Implemented APIs

### 1. Auth APIs (JWT - SimpleJWT)
- POST /api/v1/auth/register/ - User Registration
- POST /api/v1/auth/login/ - User Login (JWT) - 5h access, 1d refresh
- POST /api/v1/auth/logout/ - Logout
- POST /api/v1/auth/password-change/ - Password Change

### 2. Profile APIs
- GET /api/profile/ - Get User Profile
- PUT /api/profile/update/ - Update Profile
- POST /api/profile/upload/ - Image Upload
- GET /api/profile/search/?q=keyword - Search Users
- GET /api/profile/?page=1 - Pagination

### 3. Ride APIs - Sep 22 Sprint
- CRUD: /api/v1/rides/ - Create, List, Retrieve
- Search: Haversine 1.54km driver matching
- Filtering: ?min_fare=&max_fare=&status=&ride_type=
- Pagination & Sorting
- Booking Model + APIs + Validation
- Status Flow: REQUESTED -> ACCEPTED -> ONGOING -> COMPLETED
- PATCH /api/rides/{id}/status/ - Update ride status
- Fare Estimate: 250 for Nellore-Tirupati

### 4. Ride History & Cancel
- Ride History APIs - 4 endpoints (401 without token - expected)
- Ride Cancelled API Proof: docs/api-proof.png

## Tech Stack
- Python, Django, Django REST Framework, Channels
- JWT Authentication (rest_framework_simplejwt)
- SQLite (Local) / PostgreSQL (Prod)
- Deployed on Render

## Testing - TASK 7 DONE ✅

### Automated Testing - 10 Modules x 2 Scenarios = 20/20 PASS
```bash
python manage.py check
# System check identified no issues (0 silenced).

python manage.py test rides.tests -v 0
# Ran 20 tests in 11.886s - OK