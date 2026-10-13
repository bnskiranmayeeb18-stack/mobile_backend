from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class BookingStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    CONFIRMED = 'CONFIRMED', 'Confirmed'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    COMPLETED = 'COMPLETED', 'Completed'
    CANCELLED = 'CANCELLED', 'Cancelled'
    PAYMENT_FAILED = 'PAYMENT_FAILED', 'Payment Failed'


# Valid transitions map - TASK 2
VALID_TRANSITIONS = {
    BookingStatus.PENDING: [BookingStatus.CONFIRMED, BookingStatus.CANCELLED, BookingStatus.PAYMENT_FAILED],
    BookingStatus.CONFIRMED: [BookingStatus.IN_PROGRESS, BookingStatus.CANCELLED],
    BookingStatus.IN_PROGRESS: [BookingStatus.COMPLETED],
    BookingStatus.COMPLETED: [],
    BookingStatus.CANCELLED: [],
    BookingStatus.PAYMENT_FAILED: [],
}


class Booking(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='provided_bookings')

    service_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=BookingStatus.choices, default=BookingStatus.PENDING)

    # TASK 7 - Data Integrity
    idempotency_key = models.CharField(max_length=100, unique=True, null=True, blank=True)  # Duplicate prevention
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Required field

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['customer', 'idempotency_key'], name='unique_idempotency_per_customer'),
        ]

    def can_transition_to(self, new_status):
        return new_status in VALID_TRANSITIONS.get(self.status, [])

    def clean(self):
        # Valid statuses already handled by choices
        pass

    def __str__(self):
        return f"{self.id} - {self.status}"