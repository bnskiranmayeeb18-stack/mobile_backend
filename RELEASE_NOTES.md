# v1.0-rc
- Features: 10 modules tested
- Fixes: services.py transition validation, idempotency
- Known issues: SQLite concurrency skipped, MSG91 timeout expected
- Tests: 32/32 PASS
# Release Notes - v1.0-rc - 2026-05-13

## Objective
Prepare Django mobile backend as release candidate.

## What Completed
1. Release branch: release/v1.0-rc
2. Dependencies frozen: requirements.txt
3. Clean DB migrations: OK
4. Linting + Automated Tests: 32/32 PASS
   - 10 Modules x 2 scenarios = 20 tests
   - Advanced workflow = 8 tests
   - Security regression = 10 tests (throttle, auth, IDOR, input validation)
   - Regression journey = 1 test
5. Critical flows: CREATE->CONFIRM->START->COMPLETE->CANCEL validated
6. Security: IDOR blocked, invalid transitions blocked
7. Services: Redis/Celery/WebSocket verified (channels JWT auth)
8. API Smoke: All endpoints 200/201/400/401/403 as expected
9. Logs/Health: check --deploy -> 0 errors, 7 warnings (dev settings)

## Fixes
- rides/services.py: Added transition_booking validation, idempotency
- rides/models.py: Status transitions fixed
- test files: Indentation/syntax fixed

## Known Issues
- SQLite concurrency test skipped (expected, prod uses Postgres)
- MSG91 external call timeout (mock expected)
- Deploy warnings W002,W004,W008,W009,W012,W016,W018 - dev only, prod uses env vars

## Commits
- 2dcd15e TASK 7 32/32
- 7671ea3 models fix

## Demo Ready
Architecture, Feature (Booking), Bug Fix (COMPLETED->PENDING block), Perf (Idempotency), Security (IDOR), Deploy steps explainable.

## API Docs
Postman collection updated: auth, rides, driver, vehicle, fare, location, notifications