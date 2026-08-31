from django.urls import path
from .views import ProfileDetailView, ProfilePhotoUploadView, ProfileListView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('profile/', ProfileDetailView.as_view(), name='profile-detail'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('profile/upload-photo/', ProfilePhotoUploadView.as_view(), name='upload-photo'),
    path('profiles/search/', ProfileListView.as_view(), name='profile-search'),
    path('profiles/', ProfileListView.as_view(), name='profile-list'),
]