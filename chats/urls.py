from django.urls import path
from chats import views

urlpatterns = [
    path('servers/', views.ServerListView.as_view()),
    path('servers/create/', views.CreateServerView.as_view()),
    path('servers/<int:server_id>/', views.ServerChatRoomListView.as_view()),
    path('servers/modify/<int:server_id>/', views.ModifyServerView.as_view()),
    path('chatlogs/<int:chatroom_id>/', views.ChatRoomLogView.as_view()),
    path('chatroom/create/<int:server_id>/', views.CreateChatRoomView.as_view()),
    path('chatroom/modify/<int:chatroom_id>/', views.ModifyChatRoomNameView.as_view()),
]