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
from pathlib import Path
from datetime import timedelta
import os, json
from django.core.exceptions import ImproperlyConfigured

class check(APIView):
    def get(self, request):
        return Response('healthcheck', status=status.HTTP_200_OK)


class test(APIView):
    def get(self, request):
        response = Response("쿠키 테스트", status=status.HTTP_200_OK)
        response.set_cookie(key='test', value='hihi', max_age=None, expires=None, path='/', domain=None, secure=False, httponly=True, samesite='None')
        
        return response


# # 로그인 토큰
# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer 


class test2(APIView):
    def get(self, request):
        temp = User.objects.last().id
        print(temp)
        
        return Response('')


class Userfuc:
    def checkusernickname(nickname, num=None):
        if num == None:
            try:
                last_user_id = User.objects.last().id
            except:
                # 처음 가입 시 objects가 없음
                last_user_id = 0
        else:
            # 중복 nickname이 있어 num 매개변수에 값이 있음
            last_user_id = num + 1
            
        num = last_user_id
        # nickname ex) carrot#1996
        if last_user_id >= 10000:
            last_user_id %= 10000
        number_nickname = str(last_user_id + 1)
        
        while len(number_nickname) < 4:
            number_nickname = '0' + number_nickname
        
        result_nickname = f'{nickname}#{number_nickname}'
        verify_nickname = User.objects.filter(nickname=result_nickname)
        
        if verify_nickname:
            return Userfuc.checkusernickname(nickname, num)
        
        return result_nickname


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
        
        request_response = requests.post(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={KAKAO_REST_API_KEY}&redirect_uri={redirect_uri}&code={authorization_code}&client_secret={CLIENT_SECRET}",
            headers={"Accept": "application/json"},
        ).json()

        kakao_access_token = request_response['access_token']

        user_request_response = requests.get(
            f"https://kapi.kakao.com/v2/user/me",
            headers={"Authorization":f"Bearer {kakao_access_token}"}).json()
        
        user_email = user_request_response['kakao_account']['email']
        user_nickname = user_request_response['properties']['nickname']
        provider = 'kakao'
        
        try:
            # user가 있는지 체크
            user = User.objects.get(email=user_email, provider=provider)

            refresh = CustomTokenObtainPairSerializer.get_token(user)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token), "msg" : "로그인 성공"}, status=status.HTTP_200_OK)
        
        except:
            # user table에 생성
            try:
                # nickname 뒤에 # 붙여주기
                afterconvert_user_nickname = Userfuc.checkusernickname(user_nickname)

                new_user = User.objects.create(
                    nickname=afterconvert_user_nickname,
                    email=user_email,
                    provider=provider
                )

                refresh = CustomTokenObtainPairSerializer.get_token(new_user)
                return Response({'refresh': str(refresh), 'access': str(refresh.access_token), "msg" : "회원가입 성공"}, status=status.HTTP_200_OK)

            except Exception as error:
                # 로그인 오류
                # 추 후 error 로그 출력은 지워야 함
                return Response({f"msg" : "로그인 오류, error log : {error}"}, status=status.HTTP_400_BAD_REQUEST)