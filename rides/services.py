from django.db import transaction
from django.core.exceptions import ValidationError
from.models import Booking, BookingStatus

class BookingService:
    @staticmethod
    @transaction.atomic
    def create_booking(customer, service_name, amount, idempotency_key=None):
        if idempotency_key:
            existing = Booking.objects.filter(customer=customer, idempotency_key=idempotency_key).first()
            if existing:
                return existing, False
        booking = Booking.objects.create(
            customer=customer,
            service_name=service_name,
            amount=amount,
            idempotency_key=idempotency_key,
            status=BookingStatus.PENDING
        )
        return booking, True

    @staticmethod
    @transaction.atomic
    def transition_booking(booking_id, new_status, provider=None):
        booking = Booking.objects.select_for_update().get(id=booking_id)
        if not booking.can_transition_to(new_status):
            raise ValidationError(f"Invalid transition: {booking.status} -> {new_status}")
        if new_status == BookingStatus.CONFIRMED and provider:
            if booking.provider and booking.provider!= provider:
                raise ValidationError("Already confirmed by another provider")
            booking.provider = provider
        booking.status = new_status
        booking.save()
        return booking

    @staticmethod
    def confirm(bid, provider): return BookingService.transition_booking(bid, BookingStatus.CONFIRMED, provider)
    @staticmethod
    def start(bid): return BookingService.transition_booking(bid, BookingStatus.IN_PROGRESS)
    @staticmethod
    def complete(bid): return BookingService.transition_booking(bid, BookingStatus.COMPLETED)
    @staticmethod
    def cancel(bid): return BookingService.transition_booking(bid, BookingStatus.CANCELLED)
    @staticmethod
    def fail_payment(bid): return BookingService.transition_booking(bid, BookingStatus.PAYMENT_FAILED)

# For old views.py compatibility
def create_booking(*args, **kwargs):
    return BookingService.create_booking(*args, **kwargs)[0]

def transition_booking(*args, **kwargs):
    return BookingService.transition_booking(*args, **kwargs)

class InvalidTransitionError(Exception):
    pass