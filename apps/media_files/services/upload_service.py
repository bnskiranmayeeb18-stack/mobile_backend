import uuid
import hashlib
from io import BytesIO
from PIL import Image
from django.core.exceptions import ValidationError

SUPPORTED_MIME = {
    "image/jpeg": ["jpg", "jpeg"],
    "image/png": ["png"],
    "image/webp": ["webp"],
}
SUPPORTED_EXT = ["jpg", "jpeg", "png", "webp"]
MAX_SIZE = 5 * 1024 * 1024
MAX_WIDTH = 4096
MAX_HEIGHT = 4096
MAX_PIXELS = 16 * 1024 * 1024
MIN_SIZE = 10
EXT_TO_MIME = {ext: mime for mime, exts in SUPPORTED_MIME.items() for ext in exts}

def generate_safe_filename(original_name: str) -> str:
    ext = original_name.rsplit(".", 1)[-1].lower() if "." in original_name else "jpg"
    if ext not in SUPPORTED_EXT:
        ext = "jpg"
    return f"{uuid.uuid4().hex}.{ext}"

def _get_file_bytes(file_obj):
    file_obj.seek(0)
    data = file_obj.read(MAX_SIZE + 1)
    file_obj.seek(0)
    return data

def inspect_upload(file_obj) -> dict:
    if file_obj.size < MIN_SIZE:
        raise ValidationError("File too small or empty")
    if file_obj.size > MAX_SIZE:
        raise ValidationError(f"File too large. Max {MAX_SIZE//(1024*1024)}MB")
    ext = file_obj.name.rsplit(".", 1)[-1].lower() if "." in file_obj.name else ""
    if ext not in SUPPORTED_EXT:
        raise ValidationError(f"Unsupported extension.{ext}. Allowed: {SUPPORTED_EXT}")
    
    data = _get_file_bytes(file_obj)
    if len(data) > MAX_SIZE:
        raise ValidationError("File exceeds limit during read")
    sha256 = hashlib.sha256(data).hexdigest()
    try:
        img = Image.open(BytesIO(data))
        img.verify()
        img = Image.open(BytesIO(data))
        width, height = img.size
        canonical_mime = Image.MIME.get(img.format) or EXT_TO_MIME.get(ext)
    except Exception as e:
        raise ValidationError(f"Invalid image content: {str(e)}")
    if width > MAX_WIDTH or height > MAX_HEIGHT:
        raise ValidationError(f"Image too large {width}x{height}, max {MAX_WIDTH}x{MAX_HEIGHT}")
    if width * height > MAX_PIXELS:
        raise ValidationError(f"Image pixel count too high - possible decompression bomb")
    if canonical_mime not in SUPPORTED_MIME:
        raise ValidationError(f"Unsupported image type {canonical_mime}")
    return {
        "original_name": file_obj.name,
        "safe_name": generate_safe_filename(file_obj.name),
        "mime": canonical_mime,
        "ext": ext,
        "size": file_obj.size,
        "width": width,
        "height": height,
        "sha256": sha256,
    }

def validate_file(file_obj):
    return inspect_upload(file_obj)
