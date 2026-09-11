import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token
from urllib.parse import parse_qs
from core.models import Ride

class RideConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.ride_id = self.scope['url_route']['kwargs']['ride_id']
        self.room_group_name = f"ride_{self.ride_id}"

        # Token auth from?token=xxx
        query_string = self.scope.get('query_string', b'').decode()
        query_params = parse_qs(query_string)
        token_key = query_params.get('token', [None])[0]

        if not token_key:
            await self.close(code=4001)
            return

        user = await self.get_user_from_token(token_key)
        if not user:
            await self.close(code=4001)
            return

        self.scope['user'] = user

        # Ownership check - Task 7
        has_access = await self.check_ride_access(self.ride_id, user)
        if not has_access:
            await self.close(code=4003)
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'ride_id': self.ride_id,
            'user': user.username
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'ride_message',
                'message': data
            }
        )

    async def ride_status_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'status_update',
            'status': event['status'],
            'ride_id': event['ride_id']
        }))

    async def driver_location_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'location_update',
            'lat': event['lat'],
            'lng': event['lng'],
            'ride_id': event['ride_id']
        }))

    async def ride_message(self, event):
        await self.send(text_data=json.dumps(event['message']))

    @database_sync_to_async
    def get_user_from_token(self, token_key):
        try:
            token = Token.objects.get(key=token_key)
            return token.user
        except Token.DoesNotExist:
            return None

    @database_sync_to_async
    def check_ride_access(self, ride_id, user):
        try:
            ride = Ride.objects.get(id=ride_id)
            # Fixed: model has driver_id not driver object
            if hasattr(ride, 'driver_id') and ride.driver_id:
                if ride.driver_id!= user.id:
                    return False
            elif hasattr(ride, 'driver') and getattr(ride, 'driver', None):
                if ride.driver!= user:
                    return False
            return True
        except Ride.DoesNotExist:
            return False