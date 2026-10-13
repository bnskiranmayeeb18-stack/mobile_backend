from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rides.serializers import BookingSerializer
from rides.services import BookingService
from rides.models import Booking
import uuid

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_booking_view(request):
    serializer = BookingSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    service_type = serializer.validated_data.get('service_type') or serializer.validated_data.get('service_name')
    price = serializer.validated_data.get('price')
    key = request.headers.get('Idempotency-Key') or str(uuid.uuid4())
    try:
        booking, created = BookingService.create_booking(
            customer=request.user,
            service_type=service_type,
            price=price,
            idempotency_key=key
        )
        return Response(BookingSerializer(booking).data, status=201 if created else 200)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_bookings_view(request):
    bookings = Booking.objects.filter(customer=request.user)
    return Response(BookingSerializer(bookings, many=True).data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retrieve_booking_view(request, pk=None, booking_id=None):
    id_val = pk or booking_id
    try:
        booking = Booking.objects.get(id=id_val, customer=request.user)
        return Response(BookingSerializer(booking).data)
    except Booking.DoesNotExist:
        return Response({'detail': 'Not found'}, status=404)
    except Exception:
        return Response({'detail': 'Invalid ID'}, status=400)

@api_view(['POST', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_status_view(request, booking_id=None, pk=None):
    id_val = booking_id or pk
    new_status = request.data.get('status')
    if not new_status:
        return Response({'error': 'status required'}, status=400)
    try:
        booking = BookingService.transition_booking(int(id_val), new_status)
        return Response(BookingSerializer(booking).data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

# Backward compatibility aliases
def create_booking(*args, **kwargs):
    return BookingService.create_booking(*args, **kwargs)

# For other URLs that may exist
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_booking_view(request, booking_id=None, pk=None):
    try:
        b = BookingService.confirm(int(booking_id or pk), request.user)
        return Response(BookingSerializer(b).data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_booking_view(request, booking_id=None, pk=None):
    try:
        b = BookingService.start(int(booking_id or pk))
        return Response(BookingSerializer(b).data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_booking_view(request, booking_id=None, pk=None):
    try:
        b = BookingService.complete(int(booking_id or pk))
        return Response(BookingSerializer(b).data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_booking_view(request, booking_id=None, pk=None):
    try:
        b = BookingService.cancel(int(booking_id or pk))
        return Response(BookingSerializer(b).data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)
