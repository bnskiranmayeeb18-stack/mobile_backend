from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse, Http404
from.models import MediaFile
from.services.upload_service import inspect_upload
from django.core.exceptions import ValidationError
import logging
logger = logging.getLogger(__name__)

class MediaUploadView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        if 'file' not in request.FILES:
            return Response({"error": "No file provided"}, status=400)
        file_obj = request.FILES['file']
        is_public = str(request.data.get('is_public', 'false')).lower() == 'true'
        try:
            meta = inspect_upload(file_obj)
        except ValidationError as e:
            logger.warning(f"Upload validation failed: {e.message}")
            return Response({"error": e.message}, status=400)
        media = MediaFile.objects.create(
            user=request.user,
            file=file_obj,
            file_size=meta['size'],
            original_name=meta['original_name'],
            safe_name=meta['safe_name'],
            mime_type=meta['mime'],
            width=meta['width'],
            height=meta['height'],
            sha256=meta['sha256'],
            is_public=is_public
        )
        media.file.name = f"media/{'public' if is_public else 'private'}/{meta['safe_name']}"
        media.save(update_fields=['file'])
        return Response({
            "id": str(media.id),
            "url": media.file.url if is_public else f"/api/media/download/{media.id}/",
            "original_name": media.original_name,
            "mime": media.mime_type,
            "size": media.file_size,
            "width": media.width,
            "height": media.height,
            "is_public": media.is_public
        }, status=201)

class MediaDownloadView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, media_id):
        try:
            media = MediaFile.objects.get(id=media_id)
        except MediaFile.DoesNotExist:
            raise Http404("File not found")
        if not media.is_public and media.user!= request.user:
            return Response({"error": "Forbidden - Private file"}, status=403)
        return FileResponse(media.file.open('rb'), as_attachment=True, filename=media.original_name, content_type=media.mime_type)

class MediaListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        files = MediaFile.objects.filter(user=request.user).order_by('-created_at')[:50]
        data = [{"id": str(f.id), "name": f.original_name, "is_public": f.is_public, "size": f.file_size, "width": f.width, "height": f.height, "mime": f.mime_type} for f in files]
        return Response(data)

class MediaDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, media_id):
        try:
            media = MediaFile.objects.get(id=media_id, user=request.user)
            media.file.delete(save=False)
            media.delete()
            return Response({"message": "Deleted"}, status=200)
        except MediaFile.DoesNotExist:
            return Response({"error": "Not found"}, status=404)
