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

        # access_token = request.data.get('access_token')

        # # 카카오 API를 이용해 사용자 정보를 얻는다.
        # url = 'https://kapi.kakao.com/v2/user/me'
        # headers = {'Authorization': f'Bearer {access_token}'}
        # response = requests.post(url, headers=headers)

        # # 응답을 확인한다.
        # if response.status_code != 200:
        #     return Response(status=status.HTTP_401_UNAUTHORIZED)

        # # 응답 데이터를 확인한다.
        # kakao_user_data = response.json()
        if authorization_code:
            return Response(authorization_code, status=status.HTTP_200_OK)
        return Response("authorization code 없음", status=status.HTTP_200_OK)