# Task 5 - Ride Status API

## Valid Transitions Implemented
- REQUESTED -> ACCEPTED, CANCELLED
- ACCEPTED -> STARTED, CANCELLED
- STARTED -> COMPLETED, CANCELLED
- COMPLETED -> [] (No transition)
- CANCELLED -> [] (No transition)

## Invalid Transitions Blocked (400)
- COMPLETED -> STARTED
- CANCELLED -> ACCEPTED
- Any backward transition

## Implementation
Used VALID_TRANSITIONS dict + can_transition() method in Ride Model