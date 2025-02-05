from rest_framework import generics
from chat.models.chatroom import ChatRoom
from chat.serializers.chatroom import ChatRoomSerializer

class ChatRoomListCreateView(generics.ListCreateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer