import requests

BASE = "http://127.0.0.1:8000"

# 1. Register / Login
print("=== LOGIN ===")
r = requests.post(f"{BASE}/api/v1/auth/login/", json={"username":"admin","password":"admin123"})
print(f"Login: {r.status_code} {r.text}")
if r.status_code != 200:
    r = requests.post(f"{BASE}/api/v1/auth/register/", json={"username":"admin","password":"admin123","email":"admin@test.com"})
    print(f"Register: {r.status_code}")
    r = requests.post(f"{BASE}/api/v1/auth/login/", json={"username":"admin","password":"admin123"})
    print(f"Login2: {r.status_code} {r.text}")

token = r.json().get('access')
if not token:
    print("TOKEN RALEDU! Response:", r.json())
    exit()

headers = {"Authorization": f"Bearer {token}"}
print(f"Token ok: {token[:20]}...")

# 2. Driver Online
print("\n=== DRIVER ONLINE ===")
r = requests.post(f"{BASE}/api/v1/rides/driver/online/", headers=headers, json={"is_online": True, "lat": 17.71, "lng": 83.31})
print(f"Online: {r.status_code} {r.text}")

# 3. Create Ride
print("\n=== CREATE RIDE ===")
r = requests.post(f"{BASE}/api/v1/rides/", headers=headers, json={
    "pickup_lat": 17.7, "pickup_lng": 83.3,
    "dest_lat": 17.8, "dest_lng": 83.4,
    "ride_type": "STANDARD"
})
print(f"Create Ride: {r.status_code} {r.text}")
ride_id = r.json().get('id') if r.status_code in [200,201] else None

# 4. Find drivers (service direct already working 1.54km)
print("\n=== TEST DONE ===")
if ride_id:
    print(f"Ride {ride_id} created - DEMO SUCCESS ✅")
else:
    print("Ride creation failed - check logs")