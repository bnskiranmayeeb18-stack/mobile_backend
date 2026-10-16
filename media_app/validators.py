import os, re
from django.core.exceptions import ValidationError
from django.conf import settings

MAX_BYTES = getattr(settings, 'MAX_UPLOAD_BYTES', 10*1024*1024)
ALLOWED_TYPES = {"image/jpeg","image/png","video/mp4","application/pdf"}
ALLOWED_EXTS = {".jpg",".jpeg",".png",".mp4",".pdf"}

def validate_file(f):
    if not f:
        raise ValidationError("Missing file")
    if f.size > MAX_BYTES:
        raise ValidationError(f"File too large max {MAX_BYTES//1024//1024}MB")
    if f.content_type not in ALLOWED_TYPES:
        raise ValidationError(f"Unsupported type {f.content_type}")
    ext = os.path.splitext(f.name)[1].lower()
    if ext not in ALLOWED_EXTS:
        raise ValidationError(f"Extension {ext} not allowed")
    # magic bytes
    header = f.read(2048)
    f.seek(0)
    if ext in [".jpg",".jpeg"] and not header.startswith(b"\xff\xd8\xff"):
        raise ValidationError("Invalid JPEG")
    if ext==".png" and not header.startswith(b"\x89PNG"):
        raise ValidationError("Invalid PNG")
    if ext==".pdf" and not header.startswith(b"%PDF"):
        raise ValidationError("Invalid PDF")
