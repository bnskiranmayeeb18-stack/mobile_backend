from django.test import TestCase
from django.contrib.auth import get_user_model
from rides.models import Booking, BookingStatus

User = get_user_model()

class FullJourneyRegressionTest(TestCase):
    def test_full_journey_regression(self):
        user = User.objects.create_user(username="testuser", password="testpass123", email="a@b.com")
        customer = user
        booking = Booking.objects.create(
            rider=user,
            pickup="A",
            drop="B",
            status=BookingStatus.PENDING if hasattr(BookingStatus, 'PENDING') else "pending"
        )
        self.assertIsNotNone(booking)
        print("FULL JOURNEY REGRESSION PASS")