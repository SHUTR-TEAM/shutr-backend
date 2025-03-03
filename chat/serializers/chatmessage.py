from rest_framework import serializers

from chat.models.chatmessage import ChatMessage

class ChatMessageSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)  # MongoDB ObjectId as string
    chat = serializers.CharField()  # Store chatroom ID as string
    sender = serializers.CharField()  # Store sender ID as string
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
