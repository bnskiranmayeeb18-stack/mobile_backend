# Media Backend - Mobile Upload/Download Flow

## Supported Formats
- image/jpeg (.jpg,.jpeg), image/png, image/webp
- Max 5MB, Max 4096x4096, Max 16MP pixels
- Min 10 bytes

## Validation Layers
1. Extension allowlist
2. Size check (streamed, not full memory)
3. Pillow verify() + re-open = real content sniff
4. Dimensions + decompression bomb check
5. SHA256 + safe uuid filename

## API
### POST /api/media/upload/
Auth: JWT Bearer
Form: file (multipart), is_public (true/false)
Success 201: {id, url, mime, size, width, height, is_public}
Errors: 400 invalid type/size/bomb, 401 auth

### GET /api/media/download/<uuid>/
Auth: JWT
Access: public = any authenticated, private = owner only else 403
Returns: FileResponse with original filename

### GET /api/media/list/ -> user scoped list
### DELETE /api/media/delete/<uuid>/ -> owner only + file.delete()

## Mobile Example (Flutter/React Native)
FormData: file + is_public
Headers: Authorization: Bearer <token>
Content-Type: multipart/form-data auto

## Cleanup
python manage.py cleanup_media -> removes DB entries where file missing on disk
Add cron: daily

## Postman
Set env: {{baseUrl}}=http://127.0.0.1:8000, {{token}}
1. Upload valid jpg -> 201
2. Upload .exe -> 400
3. Upload 6MB -> 400
4. Upload 5000x5000 -> 400 bomb error
5. Download private as other user -> 403
6. Download public as other user -> 200
