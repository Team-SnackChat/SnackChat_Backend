from django.db import models
from users.models import User
from .utils import rename_imagefile_to_uuid

class Server(models.Model):
    server_name = models.CharField(max_length=15)
    is_open = models.BooleanField()
    # True -> 공개 서버, False -> 비공개 서버
    server_profile = models.ImageField(upload_to=rename_imagefile_to_uuid, default='chats/default.PNG', blank=True, null=True)
    user = models.ManyToManyField(User, related_name='server_user')
    # chat_room = models.ManyToManyField()
    # voice_room = models.ManyToManyField()

class ChatRoom(models.Model):
    chatroom_name = models.CharField(max_length=15)

class ChatMessages(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='chatmessages_chatroom')