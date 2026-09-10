import json
from channels.generic.websocket import AsyncWebsocketConsumer


class RideConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.ride_id = self.scope['url_route']['kwargs']['ride_id']
        self.room_group_name = f'ride_{self.ride_id}'

        # Group lo join avvadam
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        print(f"WebSocket Connected: {self.ride_id}")

        # Connect ayyaka welcome message
        await self.send(text_data=json.dumps({
            "type": "connection_established",
            "message": f"Connected to ride {self.ride_id}",
            "ride_id": self.ride_id
        }))

    async def disconnect(self, close_code):
        # Group nundi leave avvadam
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"WebSocket Disconnected: {self.ride_id}")

    async def receive(self, text_data):
        # Mobile nundi message vaste
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json.get('message', '')

            # Andariki broadcast cheyadam
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'ride_update',
                    'message': message,
                    'ride_id': self.ride_id
                }
            )
        except Exception as e:
            await self.send(text_data=json.dumps({"error": str(e)}))

    async def ride_update(self, event):
        # Group nundi vachina message ni mobile ki pampadam
        await self.send(text_data=json.dumps({
            "message": event['message'],
            "ride_id": event['ride_id']
        }))