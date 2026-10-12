from django.urls import path
from. import views

urlpatterns = [
    path('', views.list_rides, name='ride-list'),
    path('create/', views.create_ride, name='ride-create'),
    path('my/', views.my_rides, name='ride-my'),
    path('<int:ride_id>/update/', views.update_ride, name='ride-update'),
    path('driver/toggle/', views.driver_toggle, name='driver-toggle'),
]
