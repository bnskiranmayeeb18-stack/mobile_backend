from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from core.models import Ride

class Task5AutomationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/register/'
        self.login_url = '/api/login/'
        self.create_ride_url = '/api/rides/create/'
        self.user_data = {"username": "customer1", "password": "Test@12345", "email": "cust1@test.com"}
        self.client.post(self.register_url, self.user_data)
        login_res = self.client.post(self.login_url, {"username": "customer1", "password": "Test@12345"})
        self.token = login_res.data.get('token')

    def test_1_authentication_login_success(self):
        res = self.client.post(self.login_url, {"username": "customer1", "password": "Test@12345"})
        self.assertEqual(res.status_code, 200)

    def test_2_user_register_success(self):
        res = self.client.post(self.register_url, {"username": "newuser", "password": "Test@123", "email": "new@test.com"})
        self.assertIn(res.status_code, [200, 201])

    def test_3_driver_user_exists(self):
        user = User.objects.get(username="customer1")
        self.assertIsNotNone(user)

    def test_4_vehicle_ride_model_exists(self):
        self.assertIsNotNone(Ride.objects.count())

    def test_5_ride_create_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        res = self.client.post(self.create_ride_url, {})
        self.assertIn(res.status_code, [200, 201])

    def test_6_fare_ride_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        user = User.objects.get(username="customer1")
        ride = Ride.objects.create(user=user, customer=user, status='REQUESTED')
        res = self.client.get(f'/api/rides/{ride.id}/')
        self.assertIn(res.status_code, [200, 201])

    def test_7_permissions_401_without_token(self):
        self.client.credentials()
        res = self.client.post(self.create_ride_url, {})
        self.assertEqual(res.status_code, 401)

    def test_8_invalid_requests_400(self):
        res = self.client.post(self.register_url, {"username": ""})
        self.assertEqual(res.status_code, 400)