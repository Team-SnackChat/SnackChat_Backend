from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 

# jwt 토큰 이메일       
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['nickname'] = user.nickname  
        # 채팅에서 쓸 user id 저장해줌
        token['user_id'] = user.id
        return token