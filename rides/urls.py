from django.urls import path
from. import views
urlpatterns = [
    path('', views.list_rides, name='ride-list'),
    path('create/', views.create_ride, name='ride-create'),
    path('sync/', views.ride_sync, name='ride-sync'),
    path('<int:pk>/', views.get_ride_safe, name='ride-detail'),
    path('<int:pk>/accept/', views.ride_accept, name='ride-accept'),
    path('<int:pk>/start/', views.ride_start, name='ride-start'),
    path('<int:pk>/complete/', views.ride_complete, name='ride-complete'),
    path('<int:pk>/cancel/', views.ride_cancel, name='ride-cancel'),
    path('bookings/', views.bookings_view, name='bookings-list'),
    path('bookings/<int:pk>/', views.bookings_view, name='bookings-int'),
    path('bookings/<str:pk>/', views.bookings_view, name='bookings-str'),
]