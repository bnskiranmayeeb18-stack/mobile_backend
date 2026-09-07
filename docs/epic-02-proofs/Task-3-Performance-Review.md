# Task 3 - API Performance Review - Kiranmayee B
Date: 03-09-2026

## Response Times Summary (Thunder Client / Postman)

| API | Endpoint | Status | Time | Result |
|-----|----------|--------|------|--------|
| task-1-01-register-customer | POST /api/register/ | 400 | 78 ms | Pass (<500ms) |
| task-1-02-login-customer | POST /api/login/ | 200 | 1.06s / 1060ms | Observe - due to bcrypt hashing |
| task-1-03-create-ride | POST /api/rides/request/ | 201 | 13 ms | Pass - Excellent |
| task-1-04-register-driver | POST /api/register/ | 400 | 7 ms | Pass |
| task-1-05-login-driver | POST /api/login/ | 200 | 1.02s / 1020ms | Observe - hashing |
| task-1-06-fare-estimate | POST /api/fare-estimate/ | 201 | 13 ms | Pass - Excellent |
| task-1-07-cancel-ride | POST /api/rides/6/cancel/ | 400 | 10 ms | Pass |

## Performance Analysis
- All core business APIs (create-ride, fare-estimate, cancel) are < 20ms - Excellent performance
- Login APIs take ~1s due to password hashing (Test@123) - Expected behaviour, acceptable
- No N+1 queries - used select_related in views
- Threshold: <500ms for ride APIs - PASSED
- Threshold: <1500ms for auth APIs - PASSED

## Optimization Done
- Database indexing on username
- Token auth cached

## Screenshots
Attached: 7 API timing screenshots from Task 1 Collection

Submitted by: Kiranmayee B