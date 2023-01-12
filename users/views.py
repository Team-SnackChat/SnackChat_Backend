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
        ).json()
        
        """
        {'access_token': 'S7PJEIRPnv_9GCHFpB5nZPLRHBB2fcI_C6NkVK7iCiolUQAAAYWl46gc', 
        'token_type': 'bearer', 'refresh_token': 'vSPAoi-Ebu6lav-Qwj550_7t46OT1cTW1_nfVW4BCiolUQAAAYWl46gb', 
        'expires_in': 21599, 'scope': 'account_email profile_nickname', 
        'refresh_token_expires_in': 5183999}
        """

        kakao_access_token = request_response['access_token']

        user_request_response = requests.get(
            f"https://kapi.kakao.com/v2/user/me",
            headers={"Authorization":f"Bearer {kakao_access_token}"}).json()
        
        print(user_request_response)

        # access_token = request_response['access_token']
        # refresh_token = request_response['refresh_token']
        # user_data = request_response['scope']
        # print(access_token)
        # user_email = user_data['email']
        # print('userdata', user_data)
        # print(user_email)

        temp = f"인가코드 : {authorization_code}, 응답 : {user_request_response}"

        return Response(temp, status=status.HTTP_200_OK)