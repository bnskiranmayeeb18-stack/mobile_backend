"""
rides/views.py - REFACTORED - Task 3 - Thin Views
Before: Fat views with DB ops, business calc, validation, conditionals, notification - 50+ lines
After: Thin views - Only permission + serializer + service call + response - 4-5 lines
Business logic moved to services/ride_service.py
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from.models import Ride
from.serializers import RideSerializer, RideStatusUpdateSerializer
from services.ride_service import RideService

class RideViewSet(viewsets.ModelViewSet):
    """
    Thin ViewSet - All business logic in RideService
    Request -> Serializer (validation) -> View (thin) -> Service (fat) -> Repository/ORM -> DB
    """
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Database operation MOVED to service - Task 3 fix
        # View only delegates to service - thin
        return RideService.get_user_rides(self.request.user)

    def perform_create(self, serializer):
        # Business calculation, validation, DB ops, notification MOVED to service
        # View thin - only 2 lines
        validated_data = serializer.validated_data
        ride = RideService.create_ride(self.request.user, validated_data)
        return ride

    def create(self, request, *args, **kwargs):
        # Override to use service
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) # Validation in serializer - Task 3
        ride = RideService.create_ride(request.user, serializer.validated_data)
        output_serializer = self.get_serializer(ride)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'], url_path='status')
    def update_status(self, request, pk=None):
        # Multiple conditional statements, notification logic, cache, WS broadcast MOVED to service
        # View thin - only 3 lines
        status_serializer = RideStatusUpdateSerializer(data=request.data)
        status_serializer.is_valid(raise_exception=True)

        new_status = status_serializer.validated_data['status']
        ride = RideService.update_ride_status(pk, new_status, request.user)

        return Response(RideSerializer(ride).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='my-rides')
    def my_rides(self, request):
        # Database operation MOVED to service
        rides = RideService.get_user_rides(request.user)
        # Fix N+1 already handled in service with select_related
        page = self.paginate_queryset(rides)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(rides, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        # Business logic for delete - check permission via service
        from django.core.exceptions import PermissionDenied
        try:
            ride = RideService.get_ride_by_id(kwargs['pk'], request.user)
            return super().destroy(request, *args, **kwargs)
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)