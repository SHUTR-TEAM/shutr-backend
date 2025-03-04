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
    name = serializers.CharField(max_length=100)
    price = serializers.FloatField()
    min_price = serializers.FloatField()
    max_price = serializers.FloatField()
    availability = serializers.DateTimeField()
    experience_level = serializers.ChoiceField(choices=["Beginner", "Intermediate", "Expert"])
    tags = serializers.ListField(child=serializers.CharField(max_length=50))
    location = serializers.CharField(max_length=100)
    reviews = serializers.IntegerField(default=0)
    rating = serializers.FloatField(min_value=0, max_value=5, default=0)
    images = serializers.ListField(child=serializers.URLField())
    description = serializers.CharField(max_length=500, allow_blank=True, required=False)
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
