# apps/rides/urls.py - Task 7 - Clear responsibility + API v1
from django.urls import path
from core.services.views import RideCreateView, RideListView, RideDetailView, RideStatusUpdateView

app_name = 'rides'

urlpatterns = [
    path('', RideListView.as_view(), name='list'),  # GET /api/v1/rides/
    path('create/', RideCreateView.as_view(), name='create'),  # POST /api/v1/rides/create/
    path('<int:ride_id>/', RideDetailView.as_view(), name='detail'),  # GET /api/v1/rides/<id>/
    path('<int:ride_id>/status/', RideStatusUpdateView.as_view(), name='status-update'),  # PATCH
]