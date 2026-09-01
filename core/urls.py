from django.urls import path, include
from rest_framework.routers import DefaultRouter
from.views import VehicleTypeViewSet, VehicleViewSet, DriverProfileViewSet

router = DefaultRouter()
router.register(r'vehicle-types', VehicleTypeViewSet)
router.register(r'vehicles', VehicleViewSet)
router.register(r'drivers', DriverProfileViewSet, basename='driver')

urlpatterns = [
    path('', include(router.urls)),
]