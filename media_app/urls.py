from django.urls import path
from.views import MediaUploadView, MediaStatusView, MediaListView
urlpatterns = [
    path('upload/', MediaUploadView.as_view(), name='media-upload'),
    path('<uuid:pk>/status/', MediaStatusView.as_view(), name='media-status'),
    path('<uuid:pk>/', MediaStatusView.as_view(), name='media-detail'),
    path('', MediaListView.as_view(), name='media-list'),
]
