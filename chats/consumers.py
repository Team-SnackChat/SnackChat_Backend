import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chats.models import Server, ChatRoom, ChatMessages
from users.models import User
from channels.db import database_sync_to_async
from datetime import datetime

class CreateRoom(AsyncWebsocketConsumer):
    # django channels authentication 로그인 관련한 인증 기능 추가해야 함
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = "chat_%s" % self.room_name
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        chatroom = text_data_json['chatroom']
        message = text_data_json['message']
        sender_id = text_data_json['sender']
        images = text_data_json['images']
        
        sender = await self.get_user_db(sender_id)
        room_object = await self.get_chatroom_db(chatroom)
        user_email = await self.get_user_email(sender_id)
        is_read = False
        sender_profile_image = sender.profile_image

        if not sender:
            print('Sender user가 조회되지 않습니다.')
            return
        if not message:
            print('message가 없습니다.')
            return
        
        id = await self.create_chat_log(room_object, sender, message, images)
        
        try:
            sender = sender.nickname.split('#')[0]
        except:
            sender = sender.email

        cur_datetime = datetime.now()
        ampm = cur_datetime.strftime('%p')

        cur_time = datetime.now().strftime('%I:%M')
        date = datetime.now().strftime('%Y년 %m월 %d일')
        cur_time = f"AM {cur_time}" if ampm == 'AM' else f"PM {cur_time}"
        

        response_json = {
            'id': id,
            'message': message,
            'sender': sender,
            'chatroom': chatroom,
            'message': message,
            'images' : f'{images}',
            'is_read': is_read,
            'cur_time': cur_time,
            'date': date,
            'email': user_email,
            'profile_image': f'{sender_profile_image}'
            }
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': json.dumps(response_json)
            }
        )

    # Receive message from room group
    async def chat_message(self, event):

        message_data = json.loads(event['message'])
        id = message_data['id']
        message = message_data['message']
        sender = message_data['sender']
        images = message_data['images']
        is_read = message_data['is_read']
        cur_time = message_data['cur_time']
        date = message_data['date']
        chatroom = message_data['chatroom']
        email = message_data['email']
        profile_image = message_data['profile_image']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "id": id,
            "message": message,
            "sender": sender,
            "images": images,
            "is_read": is_read,
            "cur_time": cur_time,
            "date": date,
            "chatroom": chatroom,
            'email': email,
            'profile_image': profile_image
            }))

    @database_sync_to_async
    def get_user_db(self, user_id):
        user = User.objects.filter(id=user_id)
        if user:
            return user[0]
        return None
    
    @database_sync_to_async
    def get_chatroom_db(self, room_id):
        room = ChatRoom.objects.filter(id=room_id)
        if room:
            return room[0]
        return None
    
    @database_sync_to_async
    def get_user_email(self, user_id):
        user = User.objects.filter(id=user_id)
        if user:
            return user[0].email
        return None
    
    @database_sync_to_async
    def create_chat_log(self, room_object, sender, message, images):
        chat_log = ChatMessages.objects.create(chatroom=room_object, sender=sender, message=message, images=images)
        return chat_log.id