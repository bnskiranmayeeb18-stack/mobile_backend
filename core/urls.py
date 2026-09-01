from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DriverProfileViewSet,
    VehicleViewSet,
    VehicleTypeViewSet,
    RideViewSet,
    RideLocationViewSet
)

router = DefaultRouter()
router.register(r'drivers', DriverProfileViewSet)
router.register(r'vehicles', VehicleViewSet)
router.register(r'vehicle-types', VehicleTypeViewSet)
router.register(r'rides', RideViewSet)
router.register(r'ride-locations', RideLocationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]