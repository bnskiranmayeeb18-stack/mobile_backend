from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.media_upload, name='media_upload'),
    path('callback/', views.media_callback, name='media_callback'),
    path('events/process/', views.media_callback, name='event_process'),
]
