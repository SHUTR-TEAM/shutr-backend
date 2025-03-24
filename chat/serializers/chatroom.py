from rest_framework import serializers

from chat.models.chatroom import ChatRoom
from user.models import Photographer, User
from user.serializers import PhotographerSerializer
# from user.serializers import UserSerializer

class ChatRoomSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)  # MongoDB ObjectId as string
    name = serializers.CharField(max_length=255, required=False)
    # participants = UserSerializer(many=True)  # Store participant IDs
    participants = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Photographer.objects.all(),
        write_only=True 
    )

    participant_details = PhotographerSerializer(source='participants', many=True, read_only=True)

    last_message = serializers.CharField(allow_null=True, required=False)  # Store last message ID

    def create(self, validated_data):
        """Create a new ChatRoom document"""
        return ChatRoom(**validated_data).save()

    def update(self, instance, validated_data):
        """Update an existing ChatRoom document"""
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance