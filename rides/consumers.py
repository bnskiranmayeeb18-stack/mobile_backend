import json
from channels.generic.websocket import AsyncWebsocketConsumer

class BookingStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.booking_id = self.scope['url_route']['kwargs']['booking_id']
        self.group_name = f"booking_{self.booking_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def booking_update(self, event):
        await self.send(text_data=json.dumps(event))

    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event))