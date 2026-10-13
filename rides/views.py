from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache
from django.db.models import Prefetch
from rides.serializers import BookingSerializer
from rides.services import BookingService
from rides.models import Booking
import uuid
import time

class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

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
        # Invalidate cache on write
        cache.delete(f"bookings_user_{request.user.id}")
        return Response(BookingSerializer(booking).data, status=201 if created else 200)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_bookings_view(request):
    # Cache check - Task 4
    cache_key = f"bookings_user_{request.user.id}_page_{request.GET.get('page', 1)}"
    cached = cache.get(cache_key)
    if cached:
        return Response(cached) # Cache hit

    # Optimized query - select_related + prefetch + index usage
    bookings_qs = Booking.objects.filter(customer=request.user).select_related(
        'customer'
    ).order_by('-created_at')

    # Pagination - Task 3
    paginator = StandardPagination()
    page = paginator.paginate_queryset(bookings_qs, request)

    # Cache miss - set with TTL 300s
    data = paginator.get_paginated_response(BookingSerializer(page, many=True).data).data
    cache.set(cache_key, data, 300)
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retrieve_booking_view(request, pk=None, booking_id=None):
    id_val = pk or booking_id
    cache_key = f"booking_{id_val}"
    cached = cache.get(cache_key)
    if cached:
        return Response(cached)

    try:
        booking = Booking.objects.select_related('customer').get(id=id_val, customer=request.user)
        data = BookingSerializer(booking).data
        cache.set(cache_key, data, 300)
        return Response(data)
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
        cache.delete(f"bookings_user_{request.user.id}")
        cache.delete(f"booking_{id_val}")
        return Response(BookingSerializer(booking).data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

def create_booking(*args, **kwargs):
    return BookingService.create_booking(*args, **kwargs)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_booking_view(request, booking_id=None, pk=None):
    try:
        b = BookingService.confirm(int(booking_id or pk), request.user)
        cache.delete(f"bookings_user_{request.user.id}")
        return Response(BookingSerializer(b).data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_booking_view(request, booking_id=None, pk=None):
    try:
        b = BookingService.start(int(booking_id or pk))
        cache.delete(f"booking_{booking_id or pk}")
        return Response(BookingSerializer(b).data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_booking_view(request, booking_id=None, pk=None):
    try:
        b = BookingService.complete(int(booking_id or pk))
        cache.delete(f"booking_{booking_id or pk}")
        return Response(BookingSerializer(b).data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_booking_view(request, booking_id=None, pk=None):
    try:
        b = BookingService.cancel(int(booking_id or pk))
        cache.delete(f"bookings_user_{request.user.id}")
        return Response(BookingSerializer(b).data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)
