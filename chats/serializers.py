from rest_framework import serializers
from .models import Server, ChatMessages, ChatRoom
from users.models import User


class ServerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = ('id', 'server_name', 'is_open', 'server_profile', 'user', 'chat_room')


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'


class RoomMessageSerializer(serializers.ModelSerializer):
    cur_time = serializers.SerializerMethodField()
    sender = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    def get_email(self, obj):
        return obj.sender.email

    def get_sender(self, obj):
        try:
            nickname = obj.sender.nickname.split('#')[0]
        except:
            return obj.sender.email
        return nickname
    
    def get_profile_image(self, obj):
        return f'{obj.sender.profile_image}'

    def get_cur_time(self, obj):
        ampm = obj.created_at.strftime('%p')
        time = obj.created_at.strftime('%I:%M')
        time = f'AM {time}' if ampm == 'AM' else f'PM {time}'
        return time
    
    def get_date(self, obj):
        return obj.created_at.strftime('%Y년 %m월 %d일')
    class Meta:
        model = ChatMessages
        fields = ('message', 'sender', 'room_id')


class ChatRoomLogSerializer(serializers.ModelSerializer):
    chatlog = RoomMessageSerializer(many=True, source='chatmessages_chatroom')
    class Meta:
        model = ChatRoom
        fields = '__all__'


class CreateServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = '__all__'