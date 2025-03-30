from rest_framework import serializers

from chat.models.chatroom import ChatRoom
from user.models import Photographer, User
from user.serializers import PhotographerSerializer, UserSerializer
# from user.serializers import UserSerializer

class ChatRoomSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255, required=False)
    
    # For write operations
    participants = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Photographer.objects.all(),
        write_only=True
    )
    
    # For read operations
    participant_details = serializers.SerializerMethodField(read_only=True)
    
    last_message = serializers.CharField(allow_null=True, required=False)
    
    def get_participant_details(self, obj):
        # Explicitly get the Photographer objects by ID
        participant_ids = [str(ref.id) if hasattr(ref, 'id') else str(ref) for ref in obj.participants]
        photographers = Photographer.objects.filter(id__in=participant_ids)
        return PhotographerSerializer(photographers, many=True).data
    
    def create(self, validated_data):
        """Create a new ChatRoom document"""
        return ChatRoom(**validated_data).save()
    
    def update(self, instance, validated_data):
        """Update an existing ChatRoom document"""
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance