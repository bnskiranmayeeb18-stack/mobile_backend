import uuid, os, re, hashlib

def safe_path(user_id, filename):
    safe = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)[:100]
    return f"media/{user_id}/{uuid.uuid4().hex}_{safe}"

def sha256sum(f, chunk=8192):
    h=hashlib.sha256()
    f.seek(0)
    for c in iter(lambda: f.read(chunk), b''):
        h.update(c)
    f.seek(0)
    return h.hexdigest()
