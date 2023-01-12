from rest_framework.views import APIView
from rest_framework import status
import requests
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from users.models import User
from users.serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView   
)
#from rest_framework.permissions import IsAuthenticated
from allauth.socialaccount.models import SocialAccount
from pathlib import Path
from datetime import timedelta
import os, json
from django.core.exceptions import ImproperlyConfigured

# 로그인 토큰
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer 


class KakaologinView(APIView):
    def post(self, request):
        authorization_code = request.data['authorization_code']
        BASE_DIR = Path(__file__).resolve().parent.parent

        secret_file = os.path.join(BASE_DIR, 'secrets.json')

        with open(secret_file, 'r') as f:
            secret = json.loads(f.read())

        def get_secret(setting, secret=secret):
            try:
                return secret[setting]
            except:
                error_msg = "Set key '{0}' in secrets.json".format(setting)
                raise ImproperlyConfigured(error_msg)

        KAKAO_REST_API_KEY = get_secret('KAKAO_REST_API_KEY')
        CLIENT_SECRET = get_secret('CLIENT_SECRET')
        redirect_uri = "http://localhost:3000/kakao-loading"
        
        print(KAKAO_REST_API_KEY)
        print(CLIENT_SECRET)
        
        request_response = requests.post(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={KAKAO_REST_API_KEY}&redirect_uri={redirect_uri}&code={authorization_code}&client_secret={CLIENT_SECRET}",
            headers={"Accept": "application/json"},
        )

        print(request_response)
        # access_token = request_response['access_token']
        # refresh_token = request_response['refresh_token']
        # user_data = request_response['scope']
        # user_email = user_data['email']
        # print('userdata', user_data)
        # print(user_email)

        return Response(request_response, status=status.HTTP_200_OK)