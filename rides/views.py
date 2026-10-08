from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
import logging

from.models import Ride
from.serializers import (
    RideSerializer,
    RideListSerializer,
    RideCreateSerializer,
    RideDetailSerializer,
    RideUpdateSerializer
)
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

# Task 3: Loggers
ride_logger = logging.getLogger('ride')
api_logger = logging.getLogger('api')
ws_logger = logging.getLogger('websocket')

class RideListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Rides'],
        summary="List all rides",
        description="""
        URL: /api/rides/
        Method: GET
        Auth: Bearer Token Required
        Success: 200 with list of rides
        Error: 401 Unauthorized, 500 Server Error
        """,
        responses={200: RideListSerializer(many=True), 401: OpenApiResponse(description="Unauthorized"), 500: OpenApiResponse(description="Server Error")}
    )
    def get(self, request):
        try:
            rides = Ride.objects.filter(rider=request.user).order_by('-created_at')
            serializer = RideListSerializer(rides, many=True)
            ride_logger.info(f"RIDE_LIST_SUCCESS user={request.user.id} count={rides.count()}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            api_logger.error(f"API_ERROR endpoint=/api/rides/ user={request.user.id} error={str(e)}")
            ride_logger.error(f"RIDE_LIST_FAILED user={request.user.id} error={str(e)}")
            return Response({"error": "Failed to fetch rides"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RideCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Rides'],
        summary="Create a new ride",
        description="""
        URL: /api/rides/create/
        Method: POST
        Auth: Bearer Token Required
        Request Body: pickup_location, drop_location, ride_type
        Success: 201 with Ride data
        Error: 400 Bad Request, 401 Unauthorized, 500 Server Error
        """,
        request=RideCreateSerializer,
        responses={
            201: RideSerializer,
            400: OpenApiResponse(description="Validation Error"),
            401: OpenApiResponse(description="Unauthorized")
        },
        examples=[
            OpenApiExample(
                'Create Ride Example',
                value={"pickup_location": "Rajahmundry", "drop_location": "Kakinada", "ride_type": "mini"},
                request_only=True
            )
        ]
    )
    def post(self, request):
        try:
            serializer = RideCreateSerializer(data=request.data)
            if serializer.is_valid():
                ride = serializer.save(rider=request.user)
                ride_logger.info(f"RIDE_CREATED ride_id={ride.id} user={request.user.id} pickup={ride.pickup}")
                return Response(RideSerializer(ride).data, status=status.HTTP_201_CREATED)

            ride_logger.warning(f"RIDE_CREATE_VALIDATION_FAILED user={request.user.id} errors={serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            ride_logger.error(f"RIDE_CREATE_FAILED user={request.user.id} error={str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RideDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Rides'],
        summary="Get ride details",
        description="URL: /api/rides/{id}/ | Method: GET | Auth: Required | Success: 200 | Error: 404, 401",
        responses={200: RideDetailSerializer, 404: OpenApiResponse(description="Not Found")}
    )
    def get(self, request, pk):
        try:
            ride = get_object_or_404(Ride, pk=pk, rider=request.user)
            serializer = RideDetailSerializer(ride)
            return Response(serializer.data)
        except Exception as e:
            ride_logger.error(f"RIDE_DETAIL_FAILED ride_id={pk} user={request.user.id} error={str(e)}")
            return Response({"error": "Ride not found"}, status=status.HTTP_404_NOT_FOUND)

class RideUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Rides'],
        summary="Update ride status - Driver Acceptance",
        description="""
        URL: /api/rides/{id}/update/
        Method: PATCH
        Auth: Bearer Token
        Request Body: status (accepted, completed, cancelled)
        Success: 200
        Error: 400, 404
        """,
        request=RideUpdateSerializer,
        responses={200: RideSerializer, 400: OpenApiResponse(description="Bad Request")}
    )
    def patch(self, request, pk):
        try:
            ride = get_object_or_404(Ride, pk=pk)
            serializer = RideUpdateSerializer(ride, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                ride_logger.info(f"RIDE_UPDATED ride_id={pk} new_status={request.data.get('status')} by_user={request.user.id}")

                # WebSocket log example
                try:
                    # websocket notify logic here
                    pass
                except Exception as ws_e:
                    ws_logger.error(f"WEBSOCKET_ERROR ride_id={pk} error={str(ws_e)}")

                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            ride_logger.error(f"RIDE_UPDATE_FAILED ride_id={pk} error={str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RideDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Rides'],
        summary="Delete/Cancel a ride",
        description="URL: /api/rides/{id}/delete/ | Method: DELETE | Auth: Required | Success: 204 | Error: 404",
        responses={204: OpenApiResponse(description="Deleted"), 404: OpenApiResponse(description="Not Found")}
    )
    def delete(self, request, pk):
        try:
            ride = get_object_or_404(Ride, pk=pk, rider=request.user)
            ride.delete()
            ride_logger.info(f"RIDE_DELETED ride_id={pk} user={request.user.id}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            ride_logger.error(f"RIDE_DELETE_FAILED ride_id={pk} error={str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
