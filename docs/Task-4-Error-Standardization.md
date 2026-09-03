# Task 4 - Error Response Standardization

All APIs follow standard format: {"error": "message"}

Examples tested:
- 400 - {"error": "user exists"}
- 400 - {"error": "Cannot cancel CANCELLED"}
- 401 - Unauthorized - Token missing
- Tested in Thunder Client

Status: Implemented in Django - Custom exception handler