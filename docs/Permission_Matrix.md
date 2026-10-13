| API | Customer | Provider | Admin | Unauth |
|---|---|---|---|---|
| POST /auth/register | ✅ | ✅ | ✅ | ✅ |
| GET /services | ✅ | ✅ | ✅ | ❌ |
| POST /bookings | ✅ | ❌ | ❌ | ❌ |
| POST /provider/services | ❌ | ✅ | ✅ | ❌ |
| GET /admin/users | ❌ | ❌ | ✅ | ❌ |
| User A -> User B Booking | ❌ REJECT 403 | - | - | - |