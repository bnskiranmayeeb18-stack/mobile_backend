import uuid, logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from.models import MediaFile
from.validators import validate_file
from.utils import sha256sum

logger = logging.getLogger(__name__)

try:
    from.tasks import process_media
except Exception:
    process_media = None

class MediaUploadView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        idem_key = request.headers.get("Idempotency-Key") or request.META.get("HTTP_IDEMPOTENCY_KEY")
        if not idem_key:
            return Response({"error":"Idempotency-Key header required","code":"missing_idempotency_key"}, status=400)

        existing = MediaFile.objects.filter(idempotency_key=idem_key, owner=request.user).first()
        if existing:
            logger.info("media_duplicate_blocked", extra={"correlation_id":str(existing.correlation_id)})
            return Response({"id":str(existing.id),"status":existing.status,"detail":"Duplicate - idempotent return","correlation_id":str(existing.correlation_id)}, status=200)

        f = request.FILES.get("file")
        if not f:
            return Response({"error":"file field required","code":"missing_file"}, status=400)
        try:
            validate_file(f)
        except ValidationError as e:
            return Response({"error":str(e.message if hasattr(e,'message') else e),"code":"invalid_file"}, status=400)

        corr = uuid.uuid4()
        obj = MediaFile.objects.create(
            owner=request.user, file=f, original_name=f.name,
            file_type=f.content_type, size=f.size,
            idempotency_key=idem_key, correlation_id=corr,
            checksum=sha256sum(f)
        )
        logger.info(f"media_upload_started user={request.user.id} size={f.size}", extra={"correlation_id":str(corr)})
        if process_media:
            try: process_media.delay(str(obj.id))
            except Exception as ex: logger.error(f"celery enqueue failed {ex}", extra={"correlation_id":str(corr)})
        return Response({"id":str(obj.id),"status":obj.status,"correlation_id":str(corr)}, status=201)

class MediaStatusView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try: obj = MediaFile.objects.get(id=pk)
        except MediaFile.DoesNotExist: return Response({"error":"Not found"}, status=404)
        if obj.owner!= request.user: raise PermissionDenied("Not your media")
        return Response({"id":str(obj.id),"status":obj.status,"correlation_id":str(obj.correlation_id),"error":obj.error_message,"original_name":obj.original_name})

class MediaListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        qs = MediaFile.objects.filter(owner=request.user).values("id","status","original_name","created_at")
        return Response(list(qs))
