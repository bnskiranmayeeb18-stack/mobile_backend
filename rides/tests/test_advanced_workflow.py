from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction
from rides.models import Booking, BookingStatus
from rides.services import BookingService

User = get_user_model()

class AdvancedWorkflowTests(TestCase):
    def setUp(self):
        self.customer = User.objects.create_user(username='cust', password='pass')
        self.provider1 = User.objects.create_user(username='prov1', password='pass')
        self.provider2 = User.objects.create_user(username='prov2', password='pass')

    def test_1_create(self):
        b, created = BookingService.create_booking(self.customer, "Cleaning", 500, "key-1")
        self.assertEqual(b.status, BookingStatus.PENDING)
        print("CREATE PASS")

    def test_2_confirm(self):
        b, _ = BookingService.create_booking(self.customer, "Cleaning", 500, "key-2")
        b = BookingService.confirm(b.id, self.provider1)
        self.assertEqual(b.status, BookingStatus.CONFIRMED)
        print("CONFIRM PASS")

    def test_3_start(self):
        b, _ = BookingService.create_booking(self.customer, "Cleaning", 500, "key-3")
        BookingService.confirm(b.id, self.provider1)
        b = BookingService.start(b.id)
        self.assertEqual(b.status, BookingStatus.IN_PROGRESS)
        print("START PASS")

    def test_4_complete(self):
        b, _ = BookingService.create_booking(self.customer, "Cleaning", 500, "key-4")
        BookingService.confirm(b.id, self.provider1)
        BookingService.start(b.id)
        b = BookingService.complete(b.id)
        self.assertEqual(b.status, BookingStatus.COMPLETED)
        print("COMPLETE PASS")

    def test_5_cancel(self):
        b, _ = BookingService.create_booking(self.customer, "Cleaning", 500, "key-5")
        b = BookingService.cancel(b.id)
        self.assertEqual(b.status, BookingStatus.CANCELLED)
        print("CANCEL PASS")

    def test_6_failure_invalid_transitions(self):
        b, _ = BookingService.create_booking(self.customer, "Cleaning", 500, "key-6")
        BookingService.confirm(b.id, self.provider1)
        BookingService.start(b.id)
        BookingService.complete(b.id)
        with self.assertRaises(ValidationError):
            BookingService.transition_booking(b.id, BookingStatus.PENDING)
        print("INVALID TRANSITION BLOCKED PASS - COMPLETED -> PENDING rejected")

    def test_7_duplicate_request_idempotency(self):
        b1, c1 = BookingService.create_booking(self.customer, "Cleaning", 500, "same-key")
        b2, c2 = BookingService.create_booking(self.customer, "Cleaning", 500, "same-key")
        self.assertEqual(b1.id, b2.id)
        self.assertTrue(c1)
        self.assertFalse(c2)
        print("IDEMPOTENCY PASS - Duplicate blocked")

    def test_8_concurrent_request(self):
        b, _ = BookingService.create_booking(self.customer, "Cleaning", 500, "key-conc")
        b1 = BookingService.confirm(b.id, self.provider1)
        self.assertEqual(b1.status, BookingStatus.CONFIRMED)
        print(f"Provider1 confirmed: {b1.id}")
        with self.assertRaises(ValidationError) as ctx:
            BookingService.confirm(b.id, self.provider2)
        print(f"Provider2 failed as expected: {ctx.exception}")
        b.refresh_from_db()
        self.assertEqual(b.provider, self.provider1)
        self.assertEqual(b.status, BookingStatus.CONFIRMED)
        print("CONCURRENCY PASS - Only one provider succeeded")
