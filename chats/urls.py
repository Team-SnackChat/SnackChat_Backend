from django.urls import path
from chats import views

urlpatterns = [
    path('servers/', views.ServerListView.as_view()),
    path('servers/<int:server_id>/', views.ServerChatRoomListView.as_view()),
    path('chatlogs/<int:chatroom_id>/', views.ChatRoomLogView.as_view()),
]