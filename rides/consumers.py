import json
import jwt
from django.conf import settings
from urllib.parse import parse_qs
from channels.generic.websocket import AsyncWebsocketConsumer

class RideConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query = self.scope.get('query_string', b'').decode()
        token = parse_qs(query).get('token', [None])[0]

        if not token:
            await self.close(code=4401)
            return
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            await self.close(code=4408)
            return
        except:
            await self.close(code=4401)
            return

        self.ride_id = self.scope['url_route']['kwargs']['ride_id']
        await self.accept()
        await self.send(text_data=json.dumps({"status": "connected", "ride_id": self.ride_id, "user_id": payload.get('user_id')}))
        print(f"CONNECTED: {self.ride_id}")

    async def disconnect(self, close_code):
        print(f"DISCONNECTED: {close_code}")

    async def receive(self, text_data):
        await self.send(text_data=text_data)