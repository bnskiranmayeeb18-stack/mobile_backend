
from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_rides, name='ride-list'),
    path('create/', views.create_ride, name='ride-create'),
    path('sync/', views.ride_sync, name='ride-sync'),
    path('<int:pk>/', views.get_ride, name='ride-detail'),
    path('<int:ride_id>/', views.get_ride, name='ride-detail-alt'),
    
    # Accept
    path('<int:pk>/accept/', views.ride_accept, name='ride-accept'),
    path('<int:ride_id>/accept/', views.accept_ride, name='accept-ride'),
    
    # Start
    path('<int:pk>/start/', views.ride_start, name='ride-start'),
    path('<int:ride_id>/start/', views.start_ride, name='start-ride'),

    # Complete
    path('<int:pk>/complete/', views.ride_complete, name='ride-complete'),
    path('<int:ride_id>/complete/', views.complete_ride, name='complete-ride'),

    # Cancel
    path('<int:pk>/cancel/', views.ride_cancel, name='ride-cancel'),
    path('<int:ride_id>/cancel/', views.cancel_ride, name='cancel-ride'),

    # Legacy - map old routes to new logic
    path('<int:pk>/update/', views.ride_start, name='ride-update'),
    path('<int:pk>/delete/', views.ride_cancel, name='ride-delete'),
]
