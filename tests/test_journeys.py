from rest_framework.test import APITestCase


class CustomerJourneyTest(APITestCase):
    def test_full_flow(self):
        reg = self.client.post('/api/v1/auth/register/', {
            "username": "customer1",
            "email": "c@test.com",
            "password": "Test@12345"
        }, format='json')

        # 404 safe print
        try:
            print("REG:", reg.status_code, reg.data)
        except AttributeError:
            print("REG:", reg.status_code, reg.content.decode()[:500])

        self.assertIn(reg.status_code, [200, 201, 400])

        login = self.client.post('/api/v1/auth/login/', {
            "username": "customer1",
            "password": "Test@12345"
        }, format='json')

        try:
            print("LOGIN:", login.status_code, login.data)
            token = login.data.get('access')
        except AttributeError:
            print("LOGIN FAIL:", login.content.decode()[:500])
            token = None

        self.assertEqual(login.status_code, 200)
        self.assertIsNotNone(token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        print("PASS")