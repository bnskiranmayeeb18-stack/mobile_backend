from django.urls import path

from .views import RideDetailView, RideListView

urlpatterns = [
    path("rides/", RideListView.as_view(), name="ride-list"),
    path(
        "rides/<int:ride_id>/",
        RideDetailView.as_view(),
        name="ride-detail",
    ),
]
