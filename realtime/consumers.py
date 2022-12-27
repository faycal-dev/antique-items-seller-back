import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from store import models


class ProductConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'tester_message',
                'tester': 'hello world'
            }
        )

    async def tester_message(self, event):
        # must have the same name as the type this message is sent afteer every connection
        tester = event['tester']
        await self.send(text_data=json.dumps({
            'tester': tester,
        }))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name

        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['slug']
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'slug': message
            }
        )

    def chat_message(self, event):
        message = event['slug']

        real_time_price = models.Product.objects.filter(slug=message)[
            0].regular_price
        self.send(text_data=json.dumps({
            'real_time_price': str(real_time_price)
        }))
