from bson import ObjectId
from rest_framework import serializers

from chat.models.chatmessage import ChatMessage

class ObjectIdField(serializers.Field):
    """Custom field to handle MongoDB ObjectId serialization."""

    def to_representation(self, value):
        """Convert ObjectId to a string for JSON responses."""
        return str(value)

    def to_internal_value(self, data):
        """Convert string back to ObjectId for internal use."""
        if not ObjectId.is_valid(data):
            raise serializers.ValidationError("Invalid ObjectId")
        return ObjectId(data)


class ChatMessageSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)  # MongoDB ObjectId as string
    chat = ObjectIdField(source='chat.id')
    sender = ObjectIdField(source='sender.id')
    text = serializers.CharField(required=False, allow_blank=True)
    media_url = serializers.CharField(required=False, allow_blank=True)
    timestamp = serializers.DateTimeField()

    def create(self, validated_data):
        """Create a new ChatMessage document"""
        return ChatMessage(**validated_data).save()

    def update(self, instance, validated_data):
        """Update an existing ChatMessage document"""
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance