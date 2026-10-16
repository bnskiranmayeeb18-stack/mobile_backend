from django.test import TestCase
from unittest.mock import patch
from media_app.models import MediaAsset
from media_app.tasks import process_media

class ReliabilityTest(TestCase):
    def test_invalid_file_rejected(self):
        # test your validator rejects exe etc
        pass

    def test_retry_no_duplicate(self):
        # call process_media twice, second should skip
        asset = MediaAsset.objects.create(
            original_filename="test.jpg",
            mime_type="image/jpeg",
            size=100,
            owner_id=1,
            processing_status=MediaAsset.Status.READY
        )
        result = process_media(asset.id, correlation_id="test-123")
        self.assertEqual(result["status"], "already_ready")

    def test_storage_failure_handling(self):
        with patch('media_app.services.get_storage_backend') as mock:
            mock.side_effect = Exception("storage down")
            # your upload view should return 500 with correlation_id
            pass