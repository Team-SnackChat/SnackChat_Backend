from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
) 
from users import views

urlpatterns = [ # jwt
    # path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'), # access 
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # refesh
    path('login/kakao/token/', views.KakaologinView.as_view(), name='kakaologinview'),
    path('check/', views.check.as_view(), name='check'),
    path('test/', views.test.as_view(), name='test'),
    path('test2/', views.test2.as_view(), name='test'),
]