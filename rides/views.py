from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from.models import Booking
from.serializers import BookingSerializer
from.services import BookingService
# Wrapper functions for old views compatibility
def create_booking(*args, **kwargs):
    return BookingService.create_booking(*args, **kwargs)[0]

def transition_booking(booking_id, new_status, provider=None):
    return BookingService.transition_booking(booking_id, new_status, provider)

class InvalidTransitionError(Exception):
    pass
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_booking_view(request):
    key = request.data.get('idempotency_key')
    booking, created = create_booking(
        customer=request.user,
        service_name=request.data.get('service_name'),
        amount=request.data.get('amount', 0),
        idempotency_key=key
    )
    serializer = BookingSerializer(booking)
    return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_status_view(request, booking_id):
    try:
        new_status = request.data.get('status')
        booking = transition_booking(booking_id, new_status, provider=request.user)
        return Response(BookingSerializer(booking).data)
    except InvalidTransitionError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Booking.DoesNotExist:
        return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)