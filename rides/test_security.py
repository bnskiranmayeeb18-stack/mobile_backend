from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
import time

User = get_user_model()

class SecurityNegativeTests(APITestCase):
    def setUp(self):
        self.userA = User.objects.create_user(username='userA', email='a@test.com', password='pass123')
        self.userB = User.objects.create_user(username='userB', email='b@test.com', password='pass123')
        self.tokenA = str(RefreshToken.for_user(self.userA).access_token)
        self.tokenB = str(RefreshToken.for_user(self.userB).access_token)

    def test_invalid_jwt(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid.token.here')
        resp = self.client.get('/api/v1/rides/')
        self.assertEqual(resp.status_code, 401)

    def test_missing_jwt(self):
        resp = self.client.get('/api/v1/rides/')
        self.assertEqual(resp.status_code, 401)

    def test_idor_ride(self):
        # UserA creates ride, UserB tries to access
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.tokenA}')
        r = self.client.post('/api/v1/rides/create/', {"pickup_location":"A","drop_location":"B","ride_type":"mini"}, format='json')
        ride_id = r.data.get('id')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.tokenB}')
        resp = self.client.get(f'/api/v1/rides/{ride_id}/')
        self.assertIn(resp.status_code, [403, 404])

    def test_expired_jwt(self):
        # Simulate expired by using wrong secret - should 401
        self.client.credentials(HTTP_AUTHORIZATION='Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjEwMDAwMDAwMDB9.invalid')
        resp = self.client.get('/api/v1/rides/')
        self.assertEqual(resp.status_code, 401)

    def test_throttling_login(self):
        for i in range(6):
            self.client.post('/api/v1/auth/login/', {"username":"a","password":"wrong"}, format='json')
        resp = self.client.post('/api/v1/auth/login/', {"username":"a","password":"wrong"}, format='json')
        self.assertEqual(resp.status_code, 429)  # Too many requests

    def test_malformed_payload(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.tokenA}')
        resp = self.client.post('/api/v1/rides/create/', {"pickup": "%%%","drop": None}, format='json')
        self.assertEqual(resp.status_code, 400)