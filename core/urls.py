from django.urls import path
from .views import RideHistoryView, RideActiveView, RideCompletedView, RideCancelledView
from .views import register_customer, login_view, create_ride, ride_status_update, ride_detail

urlpatterns = [
    # ... nee old urls - vatillo api/ lekunda chudu
    path('rides/history/', RideHistoryView.as_view(), name='ride-history'),
    path('rides/active/', RideActiveView.as_view(), name='ride-active'),
    path('rides/completed/', RideCompletedView.as_view(), name='ride-completed'),
    path('rides/cancelled/', RideCancelledView.as_view(), name='ride-cancelled'),
]