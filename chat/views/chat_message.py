from bson import ObjectId
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from chat.models.chatmessage import ChatMessage
from chat.serializers.chatmessage import ChatMessageSerializer

from django.views.decorators.csrf import csrf_exempt

# List all chat messages.
# GET /api/chat/messages
@api_view(['GET'])
@csrf_exempt
def chat_message_list(request):
    chat = request.GET.get('chat')  # Get the participant ID from query params

    if chat:
        try:
            chat = ObjectId(chat)  # Convert to ObjectId
            messages = ChatMessage.objects.filter(chat=chat).order_by('-timestamp')
        except Exception:
            return Response({"error": "Invalid chat id format"}, status=status.HTTP_400_BAD_REQUEST)

    else:
        messages = ChatMessage.objects.all().order_by('-timestamp')

    serializer = ChatMessageSerializer(messages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)