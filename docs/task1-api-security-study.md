# Task 1 - Study API Security
Date: 01-Sep-2026

## 1. Authentication vs Authorization
- Authentication = WHO you are (Login, JWT)
- Authorization = WHAT you can do (Admin/User permission)

## 2. Broken Access Control
Fix: permission_classes = [IsAuthenticated, IsAdminUser]

## 3. IDOR (BOLA)
Issue: /api/users/101 ni /api/users/102 ga marchi data chudatam
Fix: User.objects.get(id=pk, owner=request.user)

## 4. Injection
Fix: Django ORM use cheyyali, raw query vaddu

## 5. Rate Limiting
Fix: DRF Throttling - 5/min for login

## 6. Sensitive Data Exposure
Fix: password = CharField(write_only=True)

## 7. Security Headers
Fix: HTTPS, HSTS, CORS proper

## 8. Secure Password Handling
Fix: user.set_password() - never plain text