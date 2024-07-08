import json

from channels.generic.websocket import AsyncWebsocketConsumer


class PollStatsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.poll_id = self.scope["url_route"]["kwargs"]["poll_id"]
        self.group_name = f"poll_{self.poll_id}"

        await self.channel_layer.group_add(
            self.group_name, self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name, self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.group_name, {"type": "send_message", "message": message}
        )

    async def send_message(self, event):
        message = event["message"]
        if isinstance(message, dict):
            message['content'] = event.get('content', None)

        await self.send(text_data=json.dumps({"message": message}))