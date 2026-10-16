# Media Pipeline - Flow

1. **Upload**: POST /api/media/upload/ - Auth required, validates type/size
   - Allowed: image/jpeg, image/png, video/mp4 - Max 10MB image, 100MB video
   - Generates correlation_id (uuid) + secure storage name: {user_id}/{uuid}_{filename}
   
2. **Validation**: File type, size, ownership, auth
   - Invalid -> 400 {error: {code, message, correlation_id}}
   - Unauthorized -> 403
   - Duplicate submission -> idempotency key check, returns existing

3. **Storage**: S3/GCS backend via get_storage_backend()
   - Naming: user_id/uuid_filename - no overwrite
   - Access-control: owner only, presigned URLs

4. **Processing**: Celery task process_media(media_id, correlation_id)
   - Events: processing-started, processing-completed, processing-failed with correlation_id
   - Status: PENDING -> PROCESSING -> READY / FAILED
   - Idempotent: select_for_update + READY check avoids duplicate results
   - Retries: 3 with backoff, no duplicate side-effects

5. **Retrieval**: GET /api/media/{id}/ and GET /api/media/{id}/status/
   - Exposes processing_status to mobile client
   - Owner check - other users 403

Failure States: INVALID_FILE, STORAGE_ERROR, PROCESSING_TIMEOUT, FAILED - all logged with correlation_id