from django.core.cache import cache
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from.models import Ride
from.serializers import RideSerializer, RideListSerializer
from.pagination import RidePagination
from.cache_service import invalidate_ride_cache

class RideListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = RideListSerializer
    pagination_class = RidePagination

    def get_queryset(self):
        # Field name issue avoid cheyadaniki only() teesesanu
        return Ride.objects.all().order_by('-created_at')

    def list(self, request, *args, **kwargs):
        page = request.query_params.get('page', '1')
        page_size = request.query_params.get('page_size', '10')
        cache_key = f"rides_list_page_{page}_size_{page_size}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=300)
        return response

class RideDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = RideSerializer
    lookup_field = 'id'
    queryset = Ride.objects.all()

class RideCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RideSerializer
    queryset = Ride.objects.all()
    def perform_create(self, serializer):
        serializer.save()
        invalidate_ride_cache()

class RideUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RideSerializer
    lookup_field = 'id'
    queryset = Ride.objects.all()
    def perform_update(self, serializer):
        serializer.save()
        invalidate_ride_cache()

class RideDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [AllowAny]
    lookup_field = 'id'
    queryset = Ride.objects.all()
    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        invalidate_ride_cache()