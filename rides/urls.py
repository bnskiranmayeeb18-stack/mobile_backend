from django.urls import path
from. import views

urlpatterns = [
    path('', views.list_rides, name='list_rides'),
    path('<int:ride_id>/', views.get_ride, name='get_ride'),
    path('create/', views.create_ride, name='create_ride'),
    path('<int:ride_id>/update/', views.update_delete_ride, name='update_delete_ride'),
]