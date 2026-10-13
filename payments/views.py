from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from.models import Payment
from rides.models import Booking
import uuid

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def simulate_pay(self, request, pk=None):
        payment = self.get_object()
        payment.payment_status = Payment.Status.SUCCESS
        payment.transaction_id = f"TXN-{uuid.uuid4().hex[:8].upper()}"
        payment.save()
        booking = payment.booking
        if booking.can_transition('CONFIRMED'):
            booking.update_status('CONFIRMED')
        return Response({
            "message": "Payment simulation successful",
            "transaction_id": payment.transaction_id,
            "payment_status": payment.payment_status,
            "booking_status": booking.status
        })