from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import ChatRoom, Server
import json
from rest_framework.permissions import IsAuthenticated
from .serializers import ChatRoomSerializer, ServerListSerializer

# Create your views here.
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