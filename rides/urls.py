from django.urls import path
from .views import RideListAPIView, RideDetailAPIView, RideCreateAPIView, RideUpdateAPIView, RideDeleteAPIView

urlpatterns = [
    path('', RideListAPIView.as_view(), name='ride-list'),
    path('create/', RideCreateAPIView.as_view(), name='ride-create'),
    path('<int:pk>/', RideDetailAPIView.as_view(), name='ride-detail'),
    path('<int:pk>/update/', RideUpdateAPIView.as_view(), name='ride-update'),
    path('<int:pk>/delete/', RideDeleteAPIView.as_view(), name='ride-delete'),
]