from django.urls import path
from.views import RideListAPIView, RideDetailAPIView, RideCreateAPIView, RideUpdateAPIView, RideDeleteAPIView

urlpatterns = [
    path('', RideListAPIView.as_view(), name='ride-list'),
    path('<int:id>/', RideDetailAPIView.as_view(), name='ride-detail'),
    path('create/', RideCreateAPIView.as_view(), name='ride-create'),
    path('<int:id>/update/', RideUpdateAPIView.as_view(), name='ride-update'),
    path('<int:id>/delete/', RideDeleteAPIView.as_view(), name='ride-delete'),
]