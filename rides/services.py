from django.db import transaction
from.models import Ride as Booking

class BookingService:
    @staticmethod
    @transaction.atomic
    def create_booking(customer, service_name="ride", amount=0, idempotency_key=None, provider=None, **kwargs):
        ex=Booking.objects.filter(rider=customer, idempotency_key=idempotency_key).first() if idempotency_key else None
        if ex:
            return ex, False
        b=Booking.objects.create(
            rider=customer,
            pickup=kwargs.get("pickup", service_name),
            drop=kwargs.get("drop", "Test Drop"),
            driver=provider,
            idempotency_key=idempotency_key,
            status="pending"
        )
        return b, True
    @staticmethod
    def create(*a, **kw):
        b,_=BookingService.create_booking(*a, **kw)
        return b
    @staticmethod
    @transaction.atomic
    def confirm(booking_id, provider=None):
        from.models import Ride
        b=Ride.objects.select_for_update().get(id=booking_id.id if hasattr(booking_id,'id') else booking_id)
        b.status="confirmed"
        if provider: b.driver=provider
        b.save()
        return b
    @staticmethod
    @transaction.atomic
    def start(booking_id):
        from.models import Ride
        b=Ride.objects.select_for_update().get(id=booking_id.id if hasattr(booking_id,'id') else booking_id)
        b.status="in_progress"
        b.save()
        return b
    @staticmethod
    @transaction.atomic
    def complete(booking_id):
        from.models import Ride
        b=Ride.objects.select_for_update().get(id=booking_id.id if hasattr(booking_id,'id') else booking_id)
        b.status="completed"
        b.save()
        return b
