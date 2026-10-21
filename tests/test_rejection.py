
from django.test import TestCase, Client
import uuid, json
class RejectionTests(TestCase):
    def test_rejection_has_correlation(self):
        c = Client()
        cid = str(uuid.uuid4())
        resp = c.post('/api/rides/create/', {}, HTTP_X_CORRELATION_ID=cid, content_type='application/json')
        self.assertEqual(resp['X-Correlation-ID'], cid)
    def test_structured_log(self):
        c = Client()
        cid = str(uuid.uuid4())
        with self.assertLogs('correlation', level='INFO') as cm:
            c.get('/api/rides/invalid/', HTTP_X_CORRELATION_ID=cid)
            self.assertTrue(any(cid in log for log in cm.output))
    def test_unauthorized_trace(self):
        c = Client()
        cid = str(uuid.uuid4())
        resp = c.get('/api/rides/', HTTP_X_CORRELATION_ID=cid)
        self.assertIn('X-Correlation-ID', resp)
