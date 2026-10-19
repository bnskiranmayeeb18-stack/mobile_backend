import json
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from .models import Media, ProcessedEvent

IDEMPOTENCY_STORE = {}
PROCESSED_EVENTS = {}
MAX_SIZE = 2 * 1024 * 1024
ALLOWED_PREFIX = "image/"

@csrf_exempt
def media_upload(request):
    correlation_id = request.headers.get('X-Correlation-ID') or str(uuid.uuid4())
    idem_key = request.headers.get('Idempotency-Key') or request.headers.get('IDEMPOTENCY-KEY')
    if not idem_key:
        return JsonResponse({'error': 'Idempotency-Key required', 'correlation_id': correlation_id}, status=400)
    if idem_key in IDEMPOTENCY_STORE:
        data = IDEMPOTENCY_STORE[idem_key]
        return JsonResponse({'id': str(data['id']), 'status': data['status'], 'message': 'Duplicate - already processed', 'duplicate': True, 'correlation_id': correlation_id}, status=200)
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)
    file = request.FILES.get('file')
    if not file:
        return JsonResponse({'error': 'file required'}, status=400)
    if file.size > MAX_SIZE:
        return JsonResponse({'error': f'File too large. Max {MAX_SIZE} bytes'}, status=400)
    if not file.content_type.startswith(ALLOWED_PREFIX):
        return JsonResponse({'error': f'Invalid type. Allowed {ALLOWED_PREFIX}*'}, status=400)
    media = Media.objects.create(file_name=file.name, status='PENDING', size=file.size)
    result = {'id': str(media.id), 'status': media.status}
    IDEMPOTENCY_STORE[idem_key] = result
    try:
        ProcessedEvent.objects.create(event_id=idem_key, media_id=str(media.id), event_type='UPLOAD', status='PENDING', result=result, correlation_id=correlation_id)
    except IntegrityError:
        pass
    return JsonResponse({'id': str(media.id), 'status': 'PENDING', 'correlation_id': correlation_id}, status=201)

@csrf_exempt
def media_callback(request):
    correlation_id = request.headers.get('X-Correlation-ID') or str(uuid.uuid4())
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only', 'correlation_id': correlation_id}, status=405)
    try:
        data = json.loads(request.body) if request.body else {}
    except:
        return JsonResponse({'error': 'Invalid JSON', 'correlation_id': correlation_id}, status=400)
    event_id = request.headers.get('Idempotency-Key') or request.headers.get('Idempotency-key') or request.headers.get('X-Request-ID') or data.get('event_id')
    media_id = data.get('media_id')
    event_type = data.get('event_type', 'COMPLETED')
    if not event_id:
        return JsonResponse({'error': 'event_id / Idempotency-Key required', 'correlation_id': correlation_id}, status=400)
    if not media_id:
        return JsonResponse({'error': 'media_id required', 'correlation_id': correlation_id}, status=400)
    # 1. DEDUP
    if event_id in PROCESSED_EVENTS:
        return JsonResponse({'status': 'Duplicate', 'message': 'Event already processed', 'event_id': event_id, 'result': PROCESSED_EVENTS[event_id], 'duplicate': True, 'correlation_id': correlation_id}, status=200)
    existing = ProcessedEvent.objects.filter(event_id=event_id).first()
    if existing:
        PROCESSED_EVENTS[event_id] = existing.result
        return JsonResponse({'status': 'Duplicate (DB)', 'message': 'Event already processed', 'event_id': event_id, 'result': existing.result, 'duplicate': True, 'correlation_id': correlation_id}, status=200)
    # 2. OUT-OF-ORDER - Check if COMPLETED already exists for this media_id
    completed_exists = ProcessedEvent.objects.filter(media_id=media_id, event_type='COMPLETED').exists()
    if completed_exists and event_type in ['PENDING', 'PROCESSING', 'FAILED']:
        return JsonResponse({
            'status': 'Ignored - out-of-order',
            'message': f'Media {media_id} already COMPLETED, ignoring late {event_type}',
            'event_id': event_id,
            'current_status': 'COMPLETED',
            'out_of_order': True,
            'correlation_id': correlation_id
        }, status=200)
    # 3. PROCESS
    try:
        result = {'media_id': media_id, 'processed_type': event_type, 'status': 'ok', 'message': f'Processed {event_type}'}
        obj = ProcessedEvent.objects.create(event_id=event_id, media_id=media_id, event_type=event_type, status=event_type, result=result, correlation_id=correlation_id)
        PROCESSED_EVENTS[event_id] = result
        try:
            media = Media.objects.filter(id=media_id).first()
            if media and not (media.status == 'COMPLETED' and event_type != 'COMPLETED'):
                media.status = event_type
                media.save()
        except:
            pass
        return JsonResponse({'status': 'Processed', 'event_id': event_id, 'media_id': media_id, 'result': result, 'correlation_id': correlation_id}, status=201)
    except IntegrityError:
        return JsonResponse({'status': 'Duplicate (race condition)', 'event_id': event_id, 'duplicate': True, 'correlation_id': correlation_id}, status=200)
