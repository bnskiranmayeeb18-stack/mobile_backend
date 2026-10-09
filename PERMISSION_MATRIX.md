# Role & Permission Matrix

| API Endpoint | Rider | Driver | Admin |
|---|---|---|---|
| POST /register | Yes | Yes | Yes |
| POST /login | Yes | Yes | Yes |
| POST /rides/create | Yes | No | Yes |
| GET /rides/ (own) | Yes | Yes-own | All |
| PATCH /rides/{id}/accept | No | Yes | Yes |
| POST /vehicles | No | Yes | Yes |
| GET /admin/* | No | No | Yes |
| PATCH /driver/location | No | Yes | Yes |

Implemented: IsOwner, IsOwnerOrAdmin, IsDriver, IsAdmin