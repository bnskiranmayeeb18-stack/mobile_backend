import json
from channels.generic.websocket import AsyncWebsocketConsumer


class RideConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.ride_id = self.scope['url_route']['kwargs']['ride_id']
        self.room_group_name = f'ride_{self.ride_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        print(f"Connected to ride {self.ride_id}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        # Driver nundi location vasthe
        if data.get('type') == 'location_update':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'driver_location',
                    'lat': data.get('lat'),
                    'lng': data.get('lng'),
                    'heading': data.get('heading')
                }
            )
        # Status update vasthe (Task 4 kosam)
        elif data.get('type') == 'status_update':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'ride_status',
                    'status': data.get('status')
                }
            )

    # Passenger ki location pampadam
    async def driver_location(self, event):
        await self.send(text_data=json.dumps({
            'type': 'location',
            'lat': event['lat'],
            'lng': event['lng'],
            'heading': event.get('heading'),
        }))

    # Passenger ki status pampadam
    async def ride_status(self, event):
        await self.send(text_data=json.dumps({
            'status': event['status']
        }))