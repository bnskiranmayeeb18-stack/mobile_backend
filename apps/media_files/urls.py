from django.urls import path
from.views import MediaUploadView, MediaDownloadView, MediaListView, MediaDeleteView

urlpatterns = [
    path('upload/', MediaUploadView.as_view(), name='media-upload'),
    path('download/<uuid:media_id>/', MediaDownloadView.as_view(), name='media-download'),
    path('list/', MediaListView.as_view(), name='media-list'),
    path('delete/<uuid:media_id>/', MediaDeleteView.as_view(), name='media-delete'),
]
