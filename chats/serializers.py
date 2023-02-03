from rest_framework import serializers
from .models import Server, ChatMessages, ChatRoom
from users.models import User

# class Server(models.Model):
#     server_name = models.CharField(max_length=15)
#     is_open = models.BooleanField(default=False)
#     # True -> 공개 서버, False -> 비공개 서버
#     server_profile = models.ImageField(upload_to=rename_serverimagefile_to_uuid, default='chats/default.PNG', blank=True, null=True)
#     user = models.ManyToManyField(User, related_name='server_user', blank=True)
#     chat_room = models.ManyToManyField(ChatRoom, related_name='server_chat_room', blank=True)
#     # voice_room = models.ManyToManyField()

class ServerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = ('id', 'server_name', 'is_open', 'server_profile', 'user', 'chat_room')

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'