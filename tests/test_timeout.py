
from django.test import TestCase, Client
import uuid
class TimeoutTests(TestCase):
    def test_timeout_has_correlation(self):
        c = Client()
        cid = str(uuid.uuid4())
        resp = c.get('/api/rides/', HTTP_X_CORRELATION_ID=cid)
        self.assertEqual(resp['X-Correlation-ID'], cid)
    def test_log_on_request(self):
        c = Client()
        cid = str(uuid.uuid4())
        with self.assertLogs('correlation', level='INFO') as cm:
            c.get('/api/rides/', HTTP_X_CORRELATION_ID=cid)
            self.assertTrue(any(cid in log for log in cm.output))
    def test_retry_same_correlation(self):
        c = Client()
        cid = str(uuid.uuid4())
        r1 = c.get('/api/rides/', HTTP_X_CORRELATION_ID=cid)
        r2 = c.get('/api/rides/', HTTP_X_CORRELATION_ID=cid)
        self.assertEqual(r1['X-Correlation-ID'], r2['X-Correlation-ID'])
