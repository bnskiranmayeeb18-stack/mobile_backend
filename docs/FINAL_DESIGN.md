📱 Mobile App (React Native / Flutter)
        ↓ HTTPS + JWT + X-Request-ID
🌐 REST API v1 (/api/v1/)
        ↓
🔐 Authentication (JWT) - authentication app
        ↓
🛡️ Permission Layer (IsPassenger, IsDriver, IsOwner)
        ↓
⚙️ Service Layer (rides/services.py - Business Logic)
        ↓
🐘 PostgreSQL (Ride, DriverLocation, RideHistory)

Real-time:
📡 WebSocket /ws/rides/{ride_id}/ → Channels + Redis
🔄 Celery → notify_driver, notify_passenger, ride_summary
⚡ Redis → Cache driver locations, active ride, eligible drivers