from rest_framework import serializers
from bson import ObjectId
from core.models import User  # Import your MongoEngine model
import datetime

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


class UserSerializer(serializers.Serializer):
    """Custom serializer for the User model."""
    
    id = ObjectIdField(read_only=True)  # MongoDB ObjectId
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)  # Do not include in responses
    nic = serializers.CharField(max_length=50)
    phone_num = serializers.CharField(max_length=50)
    address = serializers.CharField(max_length=50, allow_blank=True, required=False)
    profile_image_url = serializers.CharField(max_length=255, allow_blank=True, required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        """Create and return a new User instance."""
        return User(**validated_data).save()

    def update(self, instance, validated_data):
        """Update and return an existing User instance."""
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.updated_at = datetime.datetime.utcnow()
        instance.save()
        return instance
