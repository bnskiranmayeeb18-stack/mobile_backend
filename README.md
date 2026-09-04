# Mobile Application Backend - Django REST Framework

## Live API
Base URL: https://mobile-backend-2kc1.onrender.com

## Swagger Documentation
- Swagger UI: https://mobile-backend-2kc1.onrender.com/swagger/
- Redoc: https://mobile-backend-2kc1.onrender.com/redoc/

## Implemented APIs

### 1. Auth APIs
- POST /api/auth/register/ - User Registration
- POST /api/auth/login/ - User Login (JWT)
- POST /api/auth/logout/ - Logout
- POST /api/auth/password-change/ - Password Change

### 2. Profile APIs
- GET /api/profile/ - Get User Profile
- PUT /api/profile/update/ - Update Profile
- POST /api/profile/upload/ - Image Upload
- GET /api/profile/search/?q=keyword - Search Users
- GET /api/profile/?page=1 - Pagination

## Tech Stack
- Python, Django, Django REST Framework
- JWT Authentication
- PostgreSQL
- Deployed on Render

## Postman Collections
All collections tested and attached in JIRA Task-7:
- Registration_Collection.json
- Login_Collection.json
- password_collection.json

## Testing
All APIs tested via Postman and Swagger - Working ✅

## Status
Sprint 9 (29/6 - 12/7) - Completed ✅
Ride Flow: REQUESTED -> ACCEPTED -> ONGOING -> COMPLETED working with PATCH /api/rides/1/status/ and fare estimate 250 for Nellore-Tirupati
- ride_collection.json - Ride lifecycle (REQUESTED->COMPLETED)
