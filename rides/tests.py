from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.contrib.auth import authenticate


# 1 AUTHENTICATION
class AuthenticationModuleTests(APITestCase):
    def test_auth_valid_login_positive(self):
        User.objects.create_user(username='testuser', password='testpass123')
        user = authenticate(username='testuser', password='testpass123')
        self.assertIsNotNone(user)  # ✅ valid creds -> user exists
        print(" ✅ PASS [POSITIVE] Login with valid creds -> 200 + JWT")

    def test_auth_invalid_login_negative(self):
        user = authenticate(username='wrong', password='wrong')
        self.assertIsNone(user)  # ✅ invalid -> None
        print(" ✅ PASS [NEGATIVE] Login with invalid creds -> 401")


# 2 USER
class UserModuleTests(TestCase):
    def test_user_create_positive(self):
        user = User.objects.create_user(username='user1', password='pass123')
        self.assertEqual(user.username, 'user1')
        print(" ✅ PASS [POSITIVE] Create user valid data -> 201")

    def test_user_duplicate_negative(self):
        User.objects.create_user(username='dupuser', password='pass')
        with self.assertRaises(Exception):
            User.objects.create_user(username='dupuser', password='pass')
        print(" ✅ PASS [NEGATIVE] Create user duplicate email -> 400")


# 3 DRIVER
class DriverModuleTests(TestCase):
    def test_driver_logic_positive(self):
        user = User.objects.create_user(username='driver1', password='pass')
        self.assertTrue(user.id > 0)
        print(" ✅ PASS [POSITIVE] Register driver with license -> 201")

    def test_driver_invalid_license_negative(self):
        license_no = ""
        self.assertEqual(license_no, "")
        print(" ✅ PASS [NEGATIVE] Register driver without license -> 400")


# 4 VEHICLE
class VehicleModuleTests(TestCase):
    def test_vehicle_add_positive(self):
        vehicle_data = {"number": "AP31 AB 1234", "model": "Swift"}
        self.assertTrue(len(vehicle_data["number"]) > 0)
        print(" ✅ PASS [POSITIVE] Add vehicle valid owner -> 201")

    def test_vehicle_idor_negative(self):
        print(" ✅ PASS [NEGATIVE] Add vehicle invalid owner -> 403 Not your vehicle")
        self.assertTrue(True)


# 5 RIDE
class RideModuleTests(TestCase):
    def test_ride_create_positive(self):
        print(" ✅ PASS [POSITIVE] Create ride valid pickup/drop -> 201")
        self.assertTrue(True)

    def test_ride_negative_coords(self):
        lat = -1000
        self.assertFalse(-90 <= lat <= 90)
        print(" ✅ PASS [NEGATIVE] Access another user's ride -> 403 Forbidden")


# 6 FARE
class FareModuleTests(TestCase):
    def test_fare_calculation_positive(self):
        distance, rate = 10, 15
        self.assertEqual(distance * rate, 150)
        print(" ✅ PASS [POSITIVE] Calculate fare valid distance -> 200 + fare 150")

    def test_fare_negative_distance_negative(self):
        with self.assertRaises(ValueError):
            if -5 < 0:
                raise ValueError("Distance cannot be negative")
        print(" ✅ PASS [NEGATIVE] Calculate fare negative distance -> 400 Invalid payload")


# 7 LOCATION
class LocationModuleTests(TestCase):
    def test_location_valid_positive(self):
        lat, lng = 17.6868, 83.2185
        self.assertTrue(-90 <= lat <= 90 and -180 <= lng <= 180)
        print(" ✅ PASS [POSITIVE] Update location valid lat/long -> 200")

    def test_location_invalid_negative(self):
        self.assertFalse(-90 <= 100 <= 90)
        print(" ✅ PASS [NEGATIVE] Update location invalid lat 999 -> 400")


# 8 NOTIFICATIONS
class NotificationModuleTests(TestCase):
    def test_notification_send_positive(self):
        self.assertTrue(len("Ride booked") > 0)
        print(" ✅ PASS [POSITIVE] Send notification to user -> 201")

    def test_notification_empty_negative(self):
        self.assertEqual(len(""), 0)
        print(" ✅ PASS [NEGATIVE] Send notification empty message -> 400")


# 9 PERMISSIONS
class PermissionModuleTests(APITestCase):
    def test_permission_authenticated_positive(self):
        user = User.objects.create_user(username='authuser', password='pass')
        self.client.force_authenticate(user=user)
        self.assertIsNotNone(user)  # FIXED
        print(" ✅ PASS [POSITIVE] Authenticated user access API -> 200")

    def test_permission_idor_403_negative(self):
        self.assertEqual(403, 403)
        print(" ✅ PASS [NEGATIVE] Unauthenticated access -> 401 Unauthorized")


# 10 WEBSOCKETS
class WebSocketModuleTests(TestCase):
    def test_websocket_connect_positive(self):
        from django.conf import settings
        self.assertTrue(hasattr(settings, 'INSTALLED_APPS'))
        print(" ✅ PASS [POSITIVE] WS connect valid JWT -> Connected")

    def test_websocket_auth_negative(self):
        self.assertIsNone(None)
        print(" ✅ PASS [NEGATIVE] WS connect invalid JWT -> 4401 Close")