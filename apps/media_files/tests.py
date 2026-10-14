from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO
from.services.upload_service import inspect_upload
from django.core.exceptions import ValidationError

User = get_user_model()

def make_image(ext='jpeg', size=(100,100)):
    buf = BytesIO()
    Image.new('RGB', size, 'red').save(buf, format=ext.upper() if ext!='jpg' else 'JPEG')
    buf.seek(0)
    return SimpleUploadedFile(f"test.{ext}", buf.read(), content_type=f"image/{ext if ext!='jpg' else 'jpeg'}")

class MediaValidationTests(TestCase):
    def test_valid_jpeg(self):
        f = make_image('jpeg')
        meta = inspect_upload(f)
        assert meta['width'] == 100

    def test_valid_png(self):
        f = make_image('png')
        meta = inspect_upload(f)
        assert meta['mime'] == 'image/png'

    def test_invalid_extension(self):
        f = SimpleUploadedFile("test.exe", b"fake", content_type="application/octet-stream")
        with self.assertRaises(ValidationError):
            inspect_upload(f)

    def test_large_file(self):
        f = SimpleUploadedFile("big.jpg", b"a"* (6*1024*1024), content_type="image/jpeg")
        with self.assertRaises(ValidationError):
            inspect_upload(f)

    def test_decompression_bomb(self):
        f = make_image(size=(5000,5000))
        with self.assertRaises(ValidationError):
            inspect_upload(f)

    def test_mime_mismatch_handled(self):
        buf = BytesIO()
        Image.new('RGB', (10,10)).save(buf, format='PNG')
        buf.seek(0)
        f = SimpleUploadedFile("test.jpg", buf.read(), content_type="image/png")
        meta = inspect_upload(f)
        assert meta['mime'] == 'image/png'
