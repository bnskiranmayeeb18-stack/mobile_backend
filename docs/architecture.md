# Mobile Backend Architecture - Final Project

```mermaid
graph TD
    A[📱 Mobile App Client<br/>iOS / Android] --> B[Django REST Framework API<br/>RESTful API - Routing - Serialization]
    B --> C[Authentication JWT<br/>Token-Based - Access & Refresh]
    C --> D[Core Modules]
    D --> D1[Rides<br/>Creation - Matching - Status]
    D --> D2[Driver<br/>Profile - Availability]
    D --> D3[Vehicle<br/>Details - Validation]
    D --> D4[Fare Calculation<br/>Pricing - Distance - Surge]
    D --> D5[Location Service<br/>GPS - Geo Updates]
    D --> D6[Notifications<br/>Push Alerts - Updates]
    D --> E[WebSocket Layer<br/>Real-Time Communication]
    E --> F[Daphne ASGI Server<br/>WebSocket Handling]
    E --> G[Channel Layer<br/>Redis - Pub/Sub]
    F --> H[(Database SQLite<br/>Users - Rides - Drivers)]
    G --> H