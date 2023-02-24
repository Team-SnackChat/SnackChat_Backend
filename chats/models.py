from django.db import models
from users.models import User
from .utils import rename_serverimagefile_to_uuid, rename_chatimagefile_to_uuid

class ChatRoom(models.Model):
    chatroom_name = models.CharField(max_length=15)

    def __str__(self):
        return f'id: {str(self.id)}, chatroom_name: {str(self.chatroom_name)}'


class Server(models.Model):
    server_name = models.CharField(max_length=15)
    is_open = models.BooleanField(default=False)
    # True -> 공개 서버, False -> 비공개 서버
    server_profile = models.ImageField(upload_to=rename_serverimagefile_to_uuid, default='chats/default.PNG', blank=True, null=True)
    # server_profile = models.ImageField(upload_to=rename_serverimagefile_to_uuid, through='server_chatroom_mediate', default='chats/default.PNG', blank=True, null=True)
    user = models.ManyToManyField(User, blank=True)
    chat_room = models.ManyToManyField(ChatRoom, on_delete=models.CASCADE, related_name='server_chat_room', blank=True)
    # voice_room = models.ManyToManyField()

    def __str__(self):
        return f'id: {str(self.id)}, server_name: {str(self.server_name)}'


# class server_chatroom_mediate(models.Model):
#     pass

class ChatMessages(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='chatmessages_chatroom')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    message = models.TextField(blank=True)
    images = models.ImageField(upload_to=rename_chatimagefile_to_uuid, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'id: {str(self.id)}, message: {str(self.message)}'