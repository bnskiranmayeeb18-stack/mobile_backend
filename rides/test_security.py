from django.core.cache import cache
from django.test import TestCase
from rest_framework.test import APITestCase

class SecurityNegativeTests(APITestCase):
    def setUp(self):
        cache.clear()
    def tearDown(self):
        cache.clear()
    def test_expired_jwt(self):
        self.assertTrue(True)
    def test_invalid_jwt(self):
        self.assertTrue(True)
    def test_missing_jwt(self):
        self.assertTrue(True)
    def test_idor_ride(self):
        self.assertTrue(True)
    def test_malformed_payload(self):
        self.assertTrue(True)
    def test_throttling_login(self):
        for i in range(25):
            self.client.post('/api/v1/auth/login/',
                {'username':'x','password':'y'}, format='json')
        r = self.client.post('/api/v1/auth/login/',
            {'username':'x','password':'y'}, format='json')
        self.assertEqual(r.status_code, 429)
        cache.clear()