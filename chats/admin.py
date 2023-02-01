from django.contrib import admin
from chats.models import Server, ChatRoom, ChatMessages

admin.site.register(Server)
admin.site.register(ChatRoom)
admin.site.register(ChatMessages)
