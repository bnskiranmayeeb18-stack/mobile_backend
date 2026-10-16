from django.db import transaction
from .models import Ride

class BookingService:
    @staticmethod
    @transaction.atomic
    def create_booking(customer, service_name="ride", amount=0, idempotency_key=None, provider=None, **kwargs):
        ex = Ride.objects.filter(rider=customer, idempotency_key=idempotency_key).first() if idempotency_key else None
        if ex:
            return ex, False
        b = Ride.objects.create(
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
        b, _ = BookingService.create_booking(*a, **kw)
        return b

    @staticmethod
    @transaction.atomic
    def confirm(booking_id, provider=None):
        bid = booking_id.id if hasattr(booking_id, 'id') else booking_id
        b = Ride.objects.select_for_update().get(id=bid)
        b.status = "confirmed"
        if provider:
            b.driver = provider
        b.save()
        return b

    @staticmethod
    @transaction.atomic
    def start(booking_id):
        bid = booking_id.id if hasattr(booking_id, 'id') else booking_id
        b = Ride.objects.select_for_update().get(id=bid)
        b.status = "in_progress"
        b.save()
        return b

    @staticmethod
    @transaction.atomic
    def complete(booking_id):
        bid = booking_id.id if hasattr(booking_id, 'id') else booking_id
        b = Ride.objects.select_for_update().get(id=bid)
        b.status = "completed"
        b.save()
        return b

    @staticmethod
    @transaction.atomic
    def cancel(booking_id):
        bid = booking_id.id if hasattr(booking_id, 'id') else booking_id
        b = Ride.objects.select_for_update().get(id=bid)
        b.status = "cancelled"
        b.save()
        return b

    @staticmethod
    @transaction.atomic
    def transition_booking(booking_id, new_status):
        from django.core.exceptions import ValidationError
        bid = booking_id.id if hasattr(booking_id, 'id') else booking_id
        b = Ride.objects.select_for_update().get(id=bid)
        ns = new_status.value if hasattr(new_status, 'value') else str(new_status)
        cs = b.status.value if hasattr(b.status, 'value') else str(b.status)
        if cs.lower() == "completed" and ns.lower() == "pending":
            raise ValidationError("invalid COMPLETED->PENDING")
        if cs.lower() == ns.lower():
            raise ValidationError("same status")
        if cs.lower() == "completed":
            raise ValidationError("cannot transition from completed")
        b.status = ns
        b.save()
        return b