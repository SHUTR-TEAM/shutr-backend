from rest_framework import serializers

from chat.models.chatroom import ChatRoom
from core.models.user import User
from core.serializers.user import UserSerializer

class ChatRoomSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)  # MongoDB ObjectId as string
    name = serializers.CharField(max_length=255, required=False)
    # participants = UserSerializer(many=True)  # Store participant IDs
    participants = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        write_only=True  # This ensures IDs are only used during write operations (create/update)
    )

    # For output: display full participant objects
    participant_details = UserSerializer(source='participants', many=True, read_only=True)

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
