
from django.test import TestCase, Client
import uuid
class OfflineModeTests(TestCase):
    def test_correlation_id_generated(self):
        c = Client()
        resp = c.get('/api/rides/')
        self.assertIn('X-Correlation-ID', resp)
    def test_client_correlation_preserved(self):
        c = Client()
        cid = str(uuid.uuid4())
        resp = c.get('/api/rides/', HTTP_X_CORRELATION_ID=cid)
        self.assertEqual(resp['X-Correlation-ID'], cid)
    def test_offline_retry_same_id(self):
        c = Client()
        cid = str(uuid.uuid4())
        r1 = c.get('/api/rides/', HTTP_X_CORRELATION_ID=cid)
        r2 = c.get('/api/rides/', HTTP_X_CORRELATION_ID=cid)
        self.assertEqual(r1['X-Correlation-ID'], r2['X-Correlation-ID'])
