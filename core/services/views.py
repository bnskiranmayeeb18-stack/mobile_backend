from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Ride
from core.services.ride_service import RideService
from core.services.serializers import (RideSerializer,
                                       RideStatusUpdateSerializer)
from core.utils.constants import MESSAGES
from core.utils.helpers import build_error_response, build_success_response


class RideCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RideSerializer(data=request.data)
        if serializer.is_valid():
            ride = RideService.create_ride(
                request.user, serializer.validated_data
            )
            return Response(
                build_success_response(
                    RideSerializer(ride).data, MESSAGES["RIDE_CREATED"]
                ),
                status=status.HTTP_201_CREATED,
            )
        return Response(
            build_error_response("Validation error", serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )


class RideListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rides = RideService.list_rides(request.user)
        return Response(
            build_success_response(RideSerializer(rides, many=True).data),
            status=status.HTTP_200_OK,
        )


class RideDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, ride_id):
        try:
            ride = RideService.get_ride(ride_id, request.user)
            return Response(
                build_success_response(RideSerializer(ride).data),
                status=status.HTTP_200_OK,
            )
        except Ride.DoesNotExist:
            return Response(
                build_error_response(MESSAGES["RIDE_NOT_FOUND"]),
                status=status.HTTP_404_NOT_FOUND,
            )


class RideStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, ride_id):
        try:
            ride = RideService.get_ride(ride_id, request.user)
            serializer = RideStatusUpdateSerializer(data=request.data)
            if serializer.is_valid():
                updated_ride = RideService.update_status(
                    ride, serializer.validated_data["status"]
                )
                return Response(
                    build_success_response(
                        RideSerializer(updated_ride).data,
                        MESSAGES["RIDE_STATUS_UPDATED"],
                    ),
                    status=status.HTTP_200_OK,
                )
            return Response(
                build_error_response("Validation error", serializer.errors),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Ride.DoesNotExist:
            return Response(
                build_error_response(MESSAGES["RIDE_NOT_FOUND"]),
                status=status.HTTP_404_NOT_FOUND,
            )
