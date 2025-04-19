import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import Message
from urllib.parse import parse_qs

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        # 从查询字符串中获取用户名
        query_params = parse_qs(self.scope["query_string"].decode('utf-8'))
        self.username = query_params.get('username', ['Anonymous'])[0]

        # 加入房间组
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        # 加载并发送历史消息
        await self.send_history_messages()

    async def disconnect(self, close_code):
        # 离开房间组
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]

        # 将消息保存到数据库
        await self.save_history_message(message, username)

        # 将消息发送到房间组
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message, "username": username}
        )

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]

        # 将消息发送到 WebSocket
        await self.send(text_data=json.dumps({"message": message, "username": username}))

    @database_sync_to_async
    def save_history_message(self, message, username):
        Message.objects.create(content=message, room=self.room_name, username=username)

    @database_sync_to_async
    def get_history_messages(self):
        return list(Message.objects.filter(room=self.room_name).values_list('content', 'username'))

    async def send_history_messages(self):
        history_messages = await self.get_history_messages()
        for message in history_messages:
            await self.send(text_data=json.dumps({"message": message[0], "username": message[1]}))

