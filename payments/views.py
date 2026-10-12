from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from rides.models import Booking
from .models import Payment
from .services import mock_process_payment
from notifications.tasks import send_notification_task


class PaymentInitiateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        booking_id = request.data.get('booking_id')
        amount = request.data.get('amount')
        booking = get_object_or_404(Booking, id=booking_id)

        # Validate: belongs to user
        if booking.user != request.user:
            return Response({"error": "Not your booking"}, status=403)
        # Validate: payable
        if booking.status != 'PENDING':
            return Response({"error": "Booking not payable"}, status=400)
        # Validate: correct amount
        if float(booking.total_amount) != float(amount):
            return Response({"error": "Amount mismatch"}, status=400)

        payment = Payment.objects.create(
            booking=booking,
            amount=amount,
            payment_method=request.data.get('payment_method', 'CARD')
        )
        # Mock processing
        result = mock_process_payment(payment)
        payment.payment_status = result
        payment.save()

        if result == Payment.Status.SUCCESS:
            booking.update_status('CONFIRMED')
            send_notification_task.delay(str(booking.user.id), "Payment Successful")
        else:
            booking.update_status('PAYMENT_FAILED')
            send_notification_task.delay(str(booking.user.id), "Payment Failed")

        return Response({
            "transaction_id": payment.transaction_id,
            "status": payment.payment_status,
            "booking_status": booking.status
        })


class PaymentWebhookView(APIView):
    permission_classes = [permissions.AllowAny]  # Webhook

    def post(self, request):
        txn_id = request.data.get('transaction_id')
        event = request.data.get('event')  # SUCCESS / FAILED
        payment = get_object_or_404(Payment, transaction_id=txn_id)

        # Validate event
        if event not in ['SUCCESS', 'FAILED']:
            return Response({"error": "Invalid event"}, status=400)

        if event == 'SUCCESS' and payment.payment_status != 'SUCCESS':
            payment.payment_status = Payment.Status.SUCCESS
            payment.save()
            payment.booking.update_status('CONFIRMED')
        elif event == 'FAILED':
            payment.payment_status = Payment.Status.FAILED
            payment.save()
            payment.booking.update_status('PAYMENT_FAILED')

        return Response({"message": "Webhook processed"})