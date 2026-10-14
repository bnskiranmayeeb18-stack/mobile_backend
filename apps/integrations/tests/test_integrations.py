from django.test import TestCase
from unittest.mock import patch
from ..services.sms_service import SMSService
from ..services.payment_service import PaymentService
from ..services.base_client import IntegrationError

class IntegrationTests(TestCase):
    def test_sms_success_mock(self):
        svc = SMSService()
        res = svc.send_otp("9876543210", "1234")
        self.assertEqual(res['type'], 'success')

    def test_sms_failure_invalid_mobile(self):
        svc = SMSService()
        with self.assertRaises(IntegrationError):
            svc.send_otp("123", "1234")

    def test_payment_success_mock(self):
        svc = PaymentService()
        res = svc.create_order(50000, "ride_123")
        self.assertEqual(res['status'], 'created')

    def test_payment_failure_invalid_amount(self):
        svc = PaymentService()
        with self.assertRaises(IntegrationError):
            svc.create_order(-100, "ride_123")

    @patch('apps.integrations.services.base_client.requests.request')
    def test_timeout_handling(self, mock_req):
        import requests
        mock_req.side_effect = requests.Timeout()
        svc = SMSService()
        svc.mock = False
        with self.assertRaises(IntegrationError):
            svc.send_otp("9876543210", "1234")
