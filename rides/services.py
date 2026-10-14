from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Booking
try:
    from .models import BookingStatus
except ImportError:
    class BookingStatus:
        PENDING='pending'
        CONFIRMED='confirmed'
        IN_PROGRESS='in_progress'
        COMPLETED='completed'
        CANCELLED='cancelled'
class InvalidTransitionError(Exception): pass
def _get(bid):
    if isinstance(bid, Booking):
        return Booking.objects.select_for_update().get(id=bid.id)
    return Booking.objects.select_for_update().get(id=bid)
class BookingService:
    @staticmethod
    @transaction.atomic
    def create_booking(customer, service_name="ride", amount=0, idempotency_key=None, provider=None, **kwargs):
        if idempotency_key:
            ex=Booking.objects.filter(customer=customer, idempotency_key=idempotency_key).first()
            if ex:
                return ex, False
        b=Booking.objects.create(customer=customer, provider=provider, service_name=kwargs.get("service", service_name), amount=amount, idempotency_key=idempotency_key, status=getattr(BookingStatus, "PENDING", "pending"))
        return b, True
    @staticmethod
    def create(*a, **kw):
        b,_=BookingService.create_booking(*a, **kw)
        return b
    @staticmethod
    @transaction.atomic
    def confirm(booking_id, provider=None):
        b=_get(booking_id)
        if str(b.status) != str(getattr(BookingStatus, "PENDING", "pending")):
            raise ValidationError("Already confirmed/cannot confirm")
        if provider:
            b.provider=provider
        b.status=getattr(BookingStatus, "CONFIRMED", "confirmed")
        b.save()
        return b
    @staticmethod
    @transaction.atomic
    def start(booking_id):
        b=_get(booking_id)
        b.status=getattr(BookingStatus, "IN_PROGRESS", "in_progress")
        b.save()
        return b
    @staticmethod
    @transaction.atomic
    def complete(booking_id):
        b=_get(booking_id)
        b.status=getattr(BookingStatus, "COMPLETED", "completed")
        b.save()
        return b
    @staticmethod
    @transaction.atomic
    def cancel(booking_id):
        b=_get(booking_id)
        b.status=getattr(BookingStatus, "CANCELLED", "cancelled")
        b.save()
        return b
    @staticmethod
    @transaction.atomic
    def transition(booking_id, new_status):
        b=_get(booking_id)
        current=str(b.status)
        new=str(new_status)
        if current==str(getattr(BookingStatus, "COMPLETED", "completed")):
            raise ValidationError("Cannot transition from completed")
        if current==str(getattr(BookingStatus, "CANCELLED", "cancelled")):
            raise ValidationError("Cannot transition from cancelled")
        if current==str(getattr(BookingStatus, "CONFIRMED", "confirmed")) and new==str(getattr(BookingStatus, "PENDING", "pending")):
            raise ValidationError("Cannot go back to pending")
        if current==str(getattr(BookingStatus, "IN_PROGRESS", "in_progress")) and new==str(getattr(BookingStatus, "PENDING", "pending")):
            raise ValidationError("Cannot go back to pending")
        b.status=new_status
        b.save()
        return b
    @staticmethod
    @transaction.atomic
    def provider_accept(bid, provider):
        b=_get(bid)
        if str(b.status) != str(getattr(BookingStatus, "PENDING", "pending")):
            raise ValidationError("Already taken")
        b.provider=provider
        b.status=getattr(BookingStatus, "CONFIRMED", "confirmed")
        b.save()
        return b
    confirm_booking=confirm
    complete_booking=complete
    cancel_booking=cancel
    transition_booking=transition
@transaction.atomic
def create_booking(customer, service_name="ride", **kw):
    b,_=BookingService.create_booking(customer, service_name, **kw)
    return b
@transaction.atomic
def transition_booking(booking, new_status):
    return BookingService.transition(booking.id if isinstance(booking, Booking) else booking, new_status)
