import os
from .base_client import BaseExternalClient, IntegrationError

class SMSService(BaseExternalClient):
    def __init__(self):
        self.mock = os.getenv('INTEGRATION_MOCK', 'True') == 'True'
        self.auth_key = os.getenv('MSG91_AUTH_KEY')
        self.flow_id = os.getenv('MSG91_FLOW_ID')

    def send_otp(self, mobile: str, otp: str) -> dict:
        if not mobile or len(mobile) < 10:
            raise IntegrationError("Invalid mobile number")
        if self.mock:
            return {"type": "success", "mock": True, "mobile": f"****{mobile[-4:]}", "otp": "****"}
        url = "https://api.msg91.com/api/v5/flow/"
        headers = {"authkey": self.auth_key}
        payload = {
            "flow_id": self.flow_id,
            "sender": os.getenv('SMS_SENDER_ID', 'MOBAPP'),
            "mobiles": f"91{mobile}",
            "VAR1": otp
        }
        return self._make_request("POST", url, json=payload, headers=headers)
