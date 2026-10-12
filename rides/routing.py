from django.urls import re_path
from rides.consumers import BookingStatusConsumer
websocket_urlpatterns = [
    re_path(r'ws/booking/(?P<booking_id>\w+)/$', BookingStatusConsumer.as_asgi()),
]