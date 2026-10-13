from django.urls import path
from . import views

urlpatterns = [
    path('bookings/', views.create_booking_view, name='booking-create'),
    path('bookings/list/', views.list_bookings_view, name='booking-list'),
    path('bookings/<str:pk>/', views.retrieve_booking_view, name='booking-detail'),
    path('bookings/<str:booking_id>/status/', views.update_status_view, name='booking-status-update'),
    path('bookings/<str:booking_id>/confirm/', views.confirm_booking_view, name='booking-confirm'),
    path('bookings/<str:booking_id>/start/', views.start_booking_view, name='booking-start'),
    path('bookings/<str:booking_id>/complete/', views.complete_booking_view, name='booking-complete'),
    path('bookings/<str:booking_id>/cancel/', views.cancel_booking_view, name='booking-cancel'),
]
