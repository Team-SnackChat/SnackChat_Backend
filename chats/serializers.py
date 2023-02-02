from rest_framework import serializers
from .models import Server, ChatMessages, ChatRoom
from users.models import User


class ServerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = '__all__'


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'