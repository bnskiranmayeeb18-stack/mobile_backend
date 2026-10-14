import os
from .base_client import BaseExternalClient, IntegrationError

class PaymentService(BaseExternalClient):
    TIMEOUT = 10
    def __init__(self):
        self.mock = os.getenv('INTEGRATION_MOCK', 'True') == 'True'
        self.key_id = os.getenv('RAZORPAY_KEY_ID')
        self.secret = os.getenv('RAZORPAY_KEY_SECRET')

    def create_order(self, amount_paise: int, receipt_id: str) -> dict:
        if amount_paise <= 0:
            raise IntegrationError("Invalid amount")
        if self.mock:
            return {"id": f"order_mock_{receipt_id}", "status": "created", "amount": amount_paise, "mock": True}
        url = "https://api.razorpay.com/v1/orders"
        auth = (self.key_id, self.secret)
        payload = {"amount": amount_paise, "currency": "INR", "receipt": receipt_id}
        return self._make_request("POST", url, json=payload, auth=auth)
