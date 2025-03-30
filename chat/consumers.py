import json
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.models.chatmessage import ChatMessage
from chat.models.chatroom import ChatRoom

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print("Received data:", text_data)
        text_data_json = json.loads(text_data)
        sender = text_data_json['sender']
        text = text_data_json['text']
        # media_url = text_data_json['media_url']

        # Save message to database
        room = ChatRoom.objects.get(id=self.room_id)
        ChatMessage.objects.create(chat=room, sender=sender, text=text)

        # Broadcast message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sender': sender,
                'text': text,
            }
        )

    async def chat_message(self, event):
        sender = event['sender']
        text = event['text']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'sender': sender,
            'text': text,
        }))