from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import ChatRoom, Server
import json
from rest_framework.permissions import IsAuthenticated
from .serializers import ChatRoomSerializer

# Create your views here.
class ServerListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        contain_user_server = user.server_user.all()
        
        return Response(contain_user_server, status=status.HTTP_200_OK)