# Task 1 - Understand Background Processing

## Synchronous Flow (Old)
API -> Process Everything -> Response
Drawback: Slow API, mobile hangs

## Asynchronous Flow (New - Celery + Redis)
API -> Create background task -> Immediate Response
Background Worker -> Process task

## Why needed for Mobile?
Mobile API should be <500ms. Heavy tasks like push notifications should be in background.

Status: Understood