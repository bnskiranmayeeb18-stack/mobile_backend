# Security Audit Report - Mobile Backend
Date: 08/Oct/2026
Tester: BlackRoth

## API Inventory
- POST /api/auth/token/, /refresh/, /blacklist/
- GET /api/rides/, GET /api/rides/<id>/, POST /api/rides/create/, PUT/DELETE /api/rides/<id>/update/
- GET /api/notifications/notifications/

## 1. JWT Security
Fix: 15min access, 7day refresh, ROTATE=True, BLACKLIST=True
Test: Invalid token 401 PASS, Old refresh {"detail":"Token is blacklisted"} PASS

## 2. IDOR HIGH
Fix: filter(rider=request.user), get_object_or_404(id=ride_id, rider=request.user)
Test: attacker cannot access other user ride -> 404 PASS

## 3. Authorization HIGH
Fix: IsAuthenticated on all views
Test: No token 401 PASS, With token 200 PASS (just now verified)

## 4. Input Validation MEDIUM
Fix: serializer.is_valid()
Test: SQLi/XSS -> 400/401 not 500 PASS

## 5. Throttling MEDIUM
Fix: Anon 10/min, User 60/min
Test: 429 Too Many Requests PASS

Acceptance: [x] IDOR, [x] AuthZ, [x] Input Validation, [x] Throttling, [x] JWT
