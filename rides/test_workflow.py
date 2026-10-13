from django.test import TestCase
from django.contrib.auth import get_user_model
from rides.models import Booking, BookingStatus
from rides.services import create_booking, transition_booking, InvalidTransitionError
import threading

User = get_user_model()

class WorkflowTests(TestCase):
    def setUp(self):
        self.customer = User.objects.create_user(username='cust', password='test123')
        self.provider1 = User.objects.create_user(username='prov1', password='test123')
        self.provider2 = User.objects.create_user(username='prov2', password='test123')

    def test_create_pending(self):
        booking, created = create_booking(self.customer, "Test Service", 100)
        self.assertEqual(booking.status, BookingStatus.PENDING)
        self.assertTrue(created)

    def test_confirm_pending_to_confirmed(self):
        booking, _ = create_booking(self.customer, "Test", 100)
        booking = transition_booking(booking.id, BookingStatus.CONFIRMED, self.provider1)
        self.assertEqual(booking.status, BookingStatus.CONFIRMED)

    def test_start_confirmed_to_in_progress(self):
        booking, _ = create_booking(self.customer, "Test", 100)
        transition_booking(booking.id, BookingStatus.CONFIRMED, self.provider1)
        booking = transition_booking(booking.id, BookingStatus.IN_PROGRESS)
        self.assertEqual(booking.status, BookingStatus.IN_PROGRESS)

    def test_complete_in_progress_to_completed(self):
        booking, _ = create_booking(self.customer, "Test", 100)
        transition_booking(booking.id, BookingStatus.CONFIRMED, self.provider1)
        transition_booking(booking.id, BookingStatus.IN_PROGRESS)
        booking = transition_booking(booking.id, BookingStatus.COMPLETED)
        self.assertEqual(booking.status, BookingStatus.COMPLETED)

    def test_cancel_pending_to_cancelled(self):
        booking, _ = create_booking(self.customer, "Test", 100)
        booking = transition_booking(booking.id, BookingStatus.CANCELLED)
        self.assertEqual(booking.status, BookingStatus.CANCELLED)

    def test_failure_pending_to_payment_failed(self):
        booking, _ = create_booking(self.customer, "Test", 100)
        booking = transition_booking(booking.id, BookingStatus.PAYMENT_FAILED)
        self.assertEqual(booking.status, BookingStatus.PAYMENT_FAILED)

    def test_invalid_completed_to_pending(self):
        booking, _ = create_booking(self.customer, "Test", 100)
        transition_booking(booking.id, BookingStatus.CONFIRMED, self.provider1)
        transition_booking(booking.id, BookingStatus.IN_PROGRESS)
        transition_booking(booking.id, BookingStatus.COMPLETED)
        with self.assertRaises(InvalidTransitionError):
            transition_booking(booking.id, BookingStatus.PENDING)

    def test_invalid_cancelled_to_completed(self):
        booking, _ = create_booking(self.customer, "Test", 100)
        transition_booking(booking.id, BookingStatus.CANCELLED)
        with self.assertRaises(InvalidTransitionError):
            transition_booking(booking.id, BookingStatus.COMPLETED)

    def test_duplicate_request_idempotency(self):
        key = "idem-key-123"
        b1, c1 = create_booking(self.customer, "Test", 100, key)
        b2, c2 = create_booking(self.customer, "Test", 100, key)
        self.assertEqual(b1.id, b2.id)
        self.assertTrue(c1)
        self.assertFalse(c2)

    def test_concurrent_request(self):
        booking, _ = create_booking(self.customer, "Test", 100)
        results = []
        def try_confirm(provider):
            try:
                b = transition_booking(booking.id, BookingStatus.CONFIRMED, provider)
                results.append('success')
            except Exception as e:
                results.append(str(e))

        # Simulate 2 providers same time
        t1 = threading.Thread(target=try_confirm, args=(self.provider1,))
        t2 = threading.Thread(target=try_confirm, args=(self.provider2,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        # One succeeds, one fails due to invalid transition
        self.assertEqual(results.count('success'), 1)