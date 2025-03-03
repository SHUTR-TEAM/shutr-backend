from django.urls import path
from chat.views.chatroom import chat_room_create, chat_room_list

urlpatterns = [
    path('chat/rooms/create', chat_room_create, name='chat_room_create'),
    path('chat/rooms', chat_room_list, name='chat_room_list'),

]