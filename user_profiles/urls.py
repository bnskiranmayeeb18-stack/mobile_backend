from django.urls import path
from .views import ProfileImageUploadView

urlpatterns = [
    path('image/', ProfileImageUploadView.as_view(), name='profile-image-upload'),
    path('upload/', ProfileImageUploadView.as_view(), name='profile-image-upload-alt'),
]
