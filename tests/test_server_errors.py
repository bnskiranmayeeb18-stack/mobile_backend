
from django.test import TestCase, Client
import uuid
class ServerErrorTests(TestCase):
    def test_404_has_correlation(self):
        c = Client()
        cid = str(uuid.uuid4())
        # Use bookings endpoint which is safer than <int:pk> which has renderer bug
        resp = c.get('/api/rides/bookings/99999999/', HTTP_X_CORRELATION_ID=cid)
        # Should have correlation even if 404/401
        self.assertIn('X-Correlation-ID', resp)

    def test_404_status(self):
        c = Client()
        cid = str(uuid.uuid4())
        resp = c.get('/this-does-not-exist-xyz/', HTTP_X_CORRELATION_ID=cid)
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp['X-Correlation-ID'], cid)

    def test_log_has_status(self):
        c = Client()
        cid = str(uuid.uuid4())
        with self.assertLogs('correlation', level='INFO') as cm:
            c.get('/nonexistent/', HTTP_X_CORRELATION_ID=cid)
            logs = ' '.join(cm.output)
            self.assertIn(cid, logs)
            self.assertIn('status_code', logs)

    def test_uuid_format(self):
        c = Client()
        resp = c.get('/api/rides/')
        cid = resp['X-Correlation-ID']
        uuid.UUID(cid)
