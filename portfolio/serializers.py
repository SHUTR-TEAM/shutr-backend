from rest_framework import serializers
from bson import ObjectId
from .models import Header, Gallery  # Import your MongoEngine model
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


class HeaderSerializer(serializers.Serializer): 
    """Custom serializer for the Header model."""
    
    id = ObjectIdField(read_only=True)  # MongoDB ObjectId
    name = serializers.CharField(max_length=41)
    Background_image_url = serializers.CharField(max_length=255, allow_blank=True, required=False)
    profile_image_url = serializers.CharField(max_length=255, allow_blank=True, required=False)

    description = serializers.CharField(max_length=1000, allow_blank=True, required=False)

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        """Create and return a new header instance."""
        return Header(**validated_data).save()

    def update(self, instance, validated_data):
        """Update and return an existing header instance."""
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.updated_at = datetime.datetime.utcnow()
        instance.save()
        return instance



class GallerySerializer(serializers.Serializer):
       """Custom serializer for the Gallery model."""
      
       id = ObjectIdField(read_only=True)
       photo_collection = serializers.ListField(child=serializers.URLField())

       def create(self, validated_data):
        """Create and return a new gallery instance."""
        return Gallery(**validated_data).save()

       def update(self, instance, validated_data):
            """Update and return an existing gallery instance."""
            for key, value in validated_data.items():
                setattr(instance, key, value)
            #instance.updated_at = datetime.datetime.utcnow()
            instance.save()
            return instance
