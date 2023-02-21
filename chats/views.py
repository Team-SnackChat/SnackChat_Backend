from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from django.db.models import Q
from .models import ChatRoom, Server
import json
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from .serializers import ChatRoomSerializer, ServerListSerializer, ChatRoomLogSerializer, CreateServerSerializer, CreateChatRoomSerialize

# 로그인된 유저의 서버방 리스트를 반환하는 함수
class ServerListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        contain_user_server = user.server_user.all()
        slz = ServerListSerializer(contain_user_server, many=True)
        if slz.data:
            return Response(slz.data, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "서버가 없습니다."}, status=status.HTTP_404_NOT_FOUND)


# 로그인된 유저 서버의 채팅방 리스트를 반환하는 함수
class ServerChatRoomListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, server_id):
        chatroom = ChatRoom.objects.filter(id=server_id)
        slz = ChatRoomSerializer(chatroom, many=True)
        if slz.data:
            return Response(slz.data, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "채팅방을 만들어 주세요"}, status=status.HTTP_404_NOT_FOUND)


class CreateServerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        slz = CreateServerSerializer(data=request.data)
        if slz.is_valid():
            slz.save(user=[request.user])
            return Response({"success": "서버를 생성하였습니다."}, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "서버 생성을 실패했습니다."}, status=status.HTTP_404_NOT_FOUND)


class ModifyServerView(APIView):
    # permission_classes = [IsAuthenticated]
    
    def put(self, request, server_id):
        server = get_object_or_404(Server, id=server_id)
        slz = CreateServerSerializer(server, data=request.data)
        if slz.is_valid():
            slz.save()
            return Response({"msg": "수정되었습니다"}, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "수정 실패했습니다"}, status=status.HTTP_400_BAD_REQUEST)


class ChatRoomLogView(APIView):
    # permission_classes = [IsAuthenticated]
    
    def get(self, request, chatroom_id):
        try:
            check_chatroom_exist = ChatRoom.objects.get(id=chatroom_id)
        except:
            return Response({"msg": "채팅방이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        slz = ChatRoomLogSerializer(check_chatroom_exist)
        
        return Response(slz.data, status=status.HTTP_200_OK)


class CreateChatRoomView(APIView):
    # permission_classes = [IsAuthenticated]
    
    def post(self, request):
        slz = CreateChatRoomSerialize(data=request.data)
        if slz.is_valid():
            slz.save()
            return Response({"success": "채팅 서버를 생성하였습니다."}, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "채팅서버 생성을 실패했습니다."}, status=status.HTTP_404_NOT_FOUND)
    

class ModifyChatRoomNameView(APIView):
    # permission_classes = [IsAuthenticated]
    
    def put(self, request, chatroom_id):
        chatroom = get_object_or_404(ChatRoom, id=chatroom_id)
        slz = CreateChatRoomSerialize(chatroom, data=request.data)
        if slz.is_valid():
            slz.save()
            return Response({"msg": "수정되었습니다"}, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "수정 실패했습니다"}, status=status.HTTP_400_BAD_REQUEST)