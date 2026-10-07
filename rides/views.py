from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.services.ride_service import RideService
from core.utils.helpers import build_success_response


class RideListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rides = RideService.get_user_rides(request.user)
        return build_success_response(rides)

    def post(self, request):
        ride = RideService.create_ride(request.user, request.data)
        return build_success_response(ride, status_code=201)


class RideDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, ride_id):
        ride = RideService.get_ride_detail(request.user, ride_id)
        return build_success_response(ride)
