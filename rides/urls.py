from django.urls import path
from. import views

urlpatterns = [
    path('', views.ride_list_create, name='ride-list'),
    path('create/', views.ride_create, name='ride-create'),
    path('<int:pk>/update/', views.ride_update, name='ride-update'),
    path('<int:pk>/accept/', views.ride_accept, name='ride-accept'),
    path('<int:pk>/start/', views.ride_start, name='ride-start'),
    path('<int:pk>/complete/', views.ride_complete, name='ride-complete'),
    path('<int:pk>/cancel/', views.ride_cancel, name='ride-cancel'),
]
