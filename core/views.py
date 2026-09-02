from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound, ValidationError
from .models import Vehicle, DriverProfile, Ride
from .serializers import VehicleSerializer, DriverProfileSerializer, RideSerializer

class CustomPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 100

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all().order_by('id')
    serializer_class = VehicleSerializer
    pagination_class = CustomPagination
    def retrieve(self, request, *args, **kwargs):
        try: return super().retrieve(request, *args, **kwargs)
        except: raise NotFound({"error": "Vehicle not found", "detail": "Vehicle with given ID does not exist", "status_code": 404})
    def create(self, request, *args, **kwargs):
        reg = request.data.get('registration_number')
        if reg and Vehicle.objects.filter(registration_number=reg).exists():
            raise ValidationError({"error": "Duplicate registration", "detail": "Vehicle already exists", "status_code": 400})
        return super().create(request, *args, **kwargs)

class DriverProfileViewSet(viewsets.ModelViewSet):
    queryset = DriverProfile.objects.all().order_by('id')
    serializer_class = DriverProfileSerializer
    pagination_class = CustomPagination
    filterset_fields = ['is_active']
    search_fields = ['name']
    def get_queryset(self):
        queryset = super().get_queryset()
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            if is_active.lower() == 'true': queryset = queryset.filter(is_active=True)
            elif is_active.lower() == 'false': queryset = queryset.filter(is_active=False)
        search = self.request.query_params.get('search')
        if search: queryset = queryset.filter(name__icontains=search)
        return queryset
    def retrieve(self, request, *args, **kwargs):
        try: return super().retrieve(request, *args, **kwargs)
        except: raise NotFound({"error": "Driver not found", "detail": "Driver with given ID does not exist", "status_code": 404})
    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        if name and DriverProfile.objects.filter(name=name).exists():
            raise ValidationError({"error": "Duplicate registration", "detail": "Driver with this name already exists", "status_code": 400})
        return super().create(request, *args, **kwargs)

class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all().order_by('id')
    serializer_class = RideSerializer
    pagination_class = CustomPagination
    def retrieve(self, request, *args, **kwargs):
        try: return super().retrieve(request, *args, **kwargs)
        except: raise NotFound({"error": "Ride not found", "detail": "Ride with given ID does not exist", "status_code": 404})

    def create(self, request, *args, **kwargs):
        pickup = request.data.get('pickup_location')
        drop = request.data.get('drop_location')
        if not pickup or not drop:
            raise ValidationError({"error": "Validation failed", "detail": "pickup_location and drop_location are required", "status_code": 400})
        ride = Ride.objects.create(
            customer_name=request.data.get('customer_name','Unknown'),
            pickup_location=pickup,
            drop_location=drop,
            ride_type=request.data.get('ride_type','standard'),
            passenger_info=request.data.get('passenger_info',{}),
            status='REQUESTED'
        )
        serializer = self.get_serializer(ride)
        return Response(serializer.data, status=status.HTTP_201_CREATED)