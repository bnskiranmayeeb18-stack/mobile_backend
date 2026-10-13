# ER Diagram
User (id, email, role: customer/provider/admin, password)
  ↓ 1-M
Profile (user_id, name, phone, avatar)
Service (id, provider_id, title, price, image)
  ↓ 1-M
Booking (id, customer_id, service_id, provider_id, status, total)
Payment (id, booking_id, amount, status: mock)
Notification (id, user_id, booking_id, message)
Location (booking_id, lat, lng, timestamp)