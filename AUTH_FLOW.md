# TASK 1 - Authentication Flow Review

## Current Implementation (from your code)
Your project uses SimpleJWT:
- `TokenObtainPairView` -> /api/v1/auth/login/
- `TokenRefreshView` -> /api/v1/auth/refresh/
- Custom `register_view` -> /api/v1/auth/register/

## Flow
1. Registration: POST /api/v1/auth/register/ {username,email,password} -> 201
2. Login: POST /api/v1/auth/login/ {username,password} -> {access, refresh}
3. API Request: Header Authorization: Bearer <access>
4. Access Token Expiry: 60 mins (settings.py) -> 401 Unauthorized -> Client must call refresh
5. Refresh: POST /api/v1/auth/refresh/ {refresh} -> new access token
6. Refresh Expiry: 7 days -> 401 -> User must login again

## What happens when token expires?
- Access expired: API returns 401. Frontend auto-calls /refresh/ with stored refresh token.
- Refresh expired: /refresh/ returns 401. Frontend clears storage, redirects to login.
- No token: DRF IsAuthenticated -> 401
- Invalid/Malformed: JWT decode fails -> 401 Invalid token

## Security Fix Implemented
- Used decouple for SECRET_KEY (no hardcode in repo)
- Short-lived access (60m) + long-lived refresh (7d) pattern