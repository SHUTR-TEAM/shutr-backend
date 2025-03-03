from bson import ObjectId
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from chat.models.chatroom import ChatRoom
from chat.serializers.chatroom import ChatRoomSerializer
from django.views.decorators.csrf import csrf_exempt

# Create a new chat room.
# POST /api/chat/rooms/create
@api_view(['POST'])
@csrf_exempt
def chat_room_create(request):
    serializer = ChatRoomSerializer(data=request.data)
    if serializer.is_valid():
        chat_room = serializer.save()
        return Response(
            {"message": "Chat room created", "room_id": str(chat_room.id)},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# List all chat rooms.
# GET /api/chat/rooms
@api_view(['GET'])
@csrf_exempt
def chat_room_list(request):
    participant_id = request.GET.get('participantId')  # Get the participant ID from query params

    if participant_id:
        try:
            participant_id = ObjectId(participant_id)  # Convert to ObjectId
        except Exception:
            return Response({"error": "Invalid participantId format"}, status=status.HTTP_400_BAD_REQUEST)

        chat_rooms = ChatRoom.objects(participants__in=[participant_id])  # MongoDB $in filter
    else:
        chat_rooms = ChatRoom.objects.all()  # Fetch all chat rooms if no filter

    serializer = ChatRoomSerializer(chat_rooms, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)