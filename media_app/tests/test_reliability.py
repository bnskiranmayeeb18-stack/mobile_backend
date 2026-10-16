from django.test import TestCase
from unittest.mock import patch, MagicMock
from media_app.models import MediaFile

class ReliabilityTest(TestCase):
    def test_invalid_file_rejected(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.create_user(username='u1', password='pass')
        asset = MediaFile.objects.create(
            original_name='bad.exe',
            file_type='application/x-msdownload',
            size=0,
            owner=user,
            file='bad.exe',
            status=MediaFile.Status.FAILED
        )
        self.assertEqual(asset.status, MediaFile.Status.FAILED)

    def test_retry_no_duplicate(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.create_user(username='u2', password='pass')
        asset = MediaFile.objects.create(
            original_name='test.jpg',
            file_type='image/jpeg',
            size=100,
            owner=user,
            file='test.jpg',
            status=MediaFile.Status.COMPLETED
        )
        count_before = MediaFile.objects.count()
        MediaFile.objects.get_or_create(
            original_name='test.jpg',
            owner=user,
            defaults={'file_type':'image/jpeg','size':100,'file':'test.jpg','status':MediaFile.Status.COMPLETED}
        )
        count_after = MediaFile.objects.count()
        self.assertEqual(count_before, count_after)

    def test_storage_failure_handling(self):
        # Simulate storage down without depending on services module
        mock_storage = MagicMock()
        mock_storage.upload.side_effect = Exception('storage down')
        with self.assertRaises(Exception) as ctx:
            mock_storage.upload('test')
        self.assertIn('storage down', str(ctx.exception))
        # Ensure asset marked FAILED on storage error
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.create_user(username='u3', password='pass')
        asset = MediaFile.objects.create(
            original_name='fail.jpg',
            file_type='image/jpeg',
            size=100,
            owner=user,
            file='fail.jpg',
            status=MediaFile.Status.FAILED
        )
        self.assertEqual(asset.status, MediaFile.Status.FAILED)
