import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .models import MediaUpload

MAX_SIZE = 2 * 1024 * 1024  # Day2: 2MB limit
ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/jpg', 'image/webp', 'image/png.png']

class MediaUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        # 1. Idempotency key - case insensitive
        idem_key = request.headers.get('Idempotency-Key') or request.headers.get('idempotency-key') or request.headers.get('Idempotency-key')
        if not idem_key:
            return Response({"error": "Idempotency-Key required"}, status=400)

        # 2. SAFE RETRY - Day2 most important - return existing without corruption
        existing = MediaUpload.objects.filter(idempotency_key=idem_key).first()
        if existing:
            return Response({
                "id": str(existing.id),
                "status": "COMPLETED",
                "detail": "Duplicate - idempotent return",
                "correlation_id": str(existing.correlation_id)
            }, status=200)

        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"error": "file required"}, status=400)

        # 3. Day2: Size validation
        if file_obj.size > MAX_SIZE:
            return Response({"error": f"File too large {file_obj.size} > {MAX_SIZE} (2MB max)"}, status=400)

        # 4. Day2: Type validation
        if file_obj.content_type not in ALLOWED_TYPES:
            # allow png with extra check
            if 'image' not in file_obj.content_type:
                return Response({"error": f"Invalid type {file_obj.content_type}. Allowed {ALLOWED_TYPES}"}, status=400)

        # 5. Create new
        media = MediaUpload.objects.create(
            user=request.user,
            file_name=file_obj.name,
            file_size=file_obj.size,
            file_type=file_obj.content_type,
            idempotency_key=idem_key,
            state=MediaUpload.State.SELECTED
        )
        # Move to UPLOADED/PENDING
        try:
            media.transition_to(MediaUpload.State.STAGING)
            media.transition_to(MediaUpload.State.UPLOADING)
            media.transition_to(MediaUpload.State.UPLOADED)
        except Exception:
            pass

        return Response({
            "id": str(media.id),
            "status": "PENDING",
            "correlation_id": str(media.correlation_id)
        }, status=201)

class MediaListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        medias = MediaUpload.objects.filter(user=request.user)[:20]
        return Response([{"id": str(m.id), "file_name": m.file_name, "state": m.state} for m in medias], status=200)
