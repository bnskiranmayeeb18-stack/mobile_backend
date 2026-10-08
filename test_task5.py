import requests
BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/api/auth/login/"

print("Testing Rate Limiting - 15 requests fast...")

for i in range(1, 16):
    r = requests.post(LOGIN_URL, json={"username": "passenger1", "password": "wrong"})
    print(f"{i}. Status: {r.status_code} - {r.text[:80]}")
    if r.status_code == 429:
        print(f"\n✅ PASS - Rate limiting works! Blocked at request {i}")
        break
else:
    print("\n❌ FAIL - No 429, rate limiting not configured")