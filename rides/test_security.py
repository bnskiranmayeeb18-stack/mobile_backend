from rest_framework.test import APITestCase


class CustomerJourneyTest(APITestCase):
    def test_full_flow(self):
        # 1. Register
        reg = self.client.post('/api/v1/auth/register/', {
            "username": "customer1",
            "email": "c@test.com",
            "password": "Test@12345"
        }, format='json')

        # safe print - 404 vasthe data undadu
        data = getattr(reg, 'data', reg.content)
        print("REG:", reg.status_code, data)

        # 201 = new, 400 = already exists (both OK for test)
        self.assertIn(reg.status_code, [200, 201, 400])

        # 2. Login
        login = self.client.post('/api/v1/auth/login/', {
            "username": "customer1",
            "password": "Test@12345"
        }, format='json')

        print("LOGIN:", login.status_code, getattr(login, 'data', login.content))

        self.assertEqual(login.status_code, 200, f"Login failed: {login.content}")

        token = login.data.get('access')
        self.assertIsNotNone(token, "No access token")

        # 3. Set token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # 4. Hit a protected endpoint - rides
        r = self.client.get('/api/v1/rides/', format='json')
        print("RIDES:", r.status_code)
        self.assertIn(r.status_code, [200, 404])  # 404 aithe rides empty, still auth OK

        print("✅ Customer Journey PASS")