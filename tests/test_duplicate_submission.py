
from django.test import TestCase, Client
import uuid
class DuplicateTests(TestCase):
    def test_duplicate_cid_same(self):
        c = Client()
        cid = str(uuid.uuid4())
        r1 = c.get('/api/rides/', HTTP_X_CORRELATION_ID=cid)
        r2 = c.get('/api/rides/', HTTP_X_CORRELATION_ID=cid)
        self.assertEqual(r1['X-Correlation-ID'], cid)
    def test_auto_uuid_generated(self):
        c = Client()
        r1 = c.get('/api/rides/')
        r2 = c.get('/api/rides/')
        self.assertNotEqual(r1['X-Correlation-ID'], r2['X-Correlation-ID'])
        uuid.UUID(r1['X-Correlation-ID'])
    def test_idempotency_not_500(self):
        c = Client()
        idem = str(uuid.uuid4())
        r1 = c.post('/api/rides/create/', '{}', content_type='application/json', HTTP_X_IDEMPOTENCY_KEY=idem)
        r2 = c.post('/api/rides/create/', '{}', content_type='application/json', HTTP_X_IDEMPOTENCY_KEY=idem)
        self.assertNotEqual(r1.status_code, 500)
        self.assertNotEqual(r2.status_code, 500)
