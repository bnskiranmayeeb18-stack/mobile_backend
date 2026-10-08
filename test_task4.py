import requests
BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/api/auth/login/"
CREATE_URL = f"{BASE_URL}/api/rides/create/"
GET_URL = f"{BASE_URL}/api/rides/"

r = requests.post(LOGIN_URL, json={"username": "passenger1", "password": "test123"})
token = r.json()['token']
headers = {"Authorization": f"Token {token}"}
print(f"Login OK: {token[:10]}...\n")

tests = [
    ("1. Empty Strings", {"pickup": "", "dropoff": ""}),
    ("2. Large String 10k", {"pickup": "A"*10000, "dropoff": "test"}),
    ("4. Invalid Numbers", {"pickup": "A", "dropoff": "B", "price": -999}),
    ("5. Unexpected Fields", {"pickup": "A", "dropoff": "B", "is_admin": True, "user_id": 1}),
    ("6. Invalid Date", {"pickup": "A", "dropoff": "B", "date": "2026-13-40"}),
    ("7. Invalid Coords", {"pickup": "A", "dropoff": "B", "lat": 9999, "lng": 9999}),
]

for name, payload in tests:
    resp = requests.post(CREATE_URL, json=payload, headers=headers)
    status = resp.status_code
    verdict = "✅ PASS - Safely handled" if status in [400,401,404,422] else "❌ FAIL - 500 crash!" if status==500 else f"Status {status}"
    print(f"{name}: {verdict} ({status}) -> {resp.text[:150]}")

print("\n--- 3. Invalid IDs ---")
for bad_id in ["abc", "999999", "-1"]:
    # abc ki <int:ride_id> match avvadu kabatti Django 404 istundi - adi kuda PASS e
    url = f"{GET_URL}{bad_id}/" if bad_id!="abc" else f"{GET_URL}abc/"
    resp = requests.get(url, headers=headers)
    print(f"GET id={bad_id}: {resp.status_code} {'✅ PASS' if resp.status_code!=500 else '❌ FAIL 500'} -> {resp.text[:100]}")