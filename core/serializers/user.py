# from rest_framework import serializers
# from bson import ObjectId
# from core.models import User  # Import your MongoEngine model
# import datetime

# class ObjectIdField(serializers.Field):
#     """Custom field to handle MongoDB ObjectId serialization."""

#     def to_representation(self, value):
#         """Convert ObjectId to a string for JSON responses."""
#         return str(value)

#     def to_internal_value(self, data):
#         """Convert string back to ObjectId for internal use."""
#         if not ObjectId.is_valid(data):
#             raise serializers.ValidationError("Invalid ObjectId")
#         return ObjectId(data)


# class UserSerializer(serializers.Serializer):
#     """Custom serializer for the User model."""
    
#     id = ObjectIdField(read_only=True)  # MongoDB ObjectId
#     first_name = serializers.CharField(max_length=50)
#     last_name = serializers.CharField(max_length=50)
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)  # Do not include in responses
#     nic = serializers.CharField(max_length=50)
#     phone_num = serializers.CharField(max_length=50)
#     address = serializers.CharField(max_length=50, allow_blank=True, required=False)
#     profile_image_url = serializers.CharField(max_length=255, allow_blank=True, required=False)
#     created_at = serializers.DateTimeField(read_only=True)
#     updated_at = serializers.DateTimeField(read_only=True)

#     def create(self, validated_data):
#         """Create and return a new User instance."""
#         return User(**validated_data).save()

#     def update(self, instance, validated_data):
#         """Update and return an existing User instance."""
#         for key, value in validated_data.items():
#             setattr(instance, key, value)
#         instance.updated_at = datetime.datetime.utcnow()
#         instance.save()
#         return instance


from rest_framework import serializers
from bson import ObjectId
from core.models import User  
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

    # Personal Information
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)  # Write-only for security
    nic = serializers.CharField(max_length=50)
    phone_num = serializers.CharField(max_length=50)
    address = serializers.CharField(max_length=255, allow_blank=True, required=False)
    profile_image_url = serializers.CharField(max_length=255, allow_blank=True, required=False)

    # Business/Photographer Details
    name = serializers.CharField(max_length=100)
    price = serializers.FloatField()
    min_price = serializers.FloatField()
    max_price = serializers.FloatField()
    availability = serializers.CharField()  # Stored as "YYYY-MM-DD"
    experience_level = serializers.ChoiceField(choices=["Beginner", "Intermediate", "Expert"])
    tags = serializers.ListField(child=serializers.CharField(max_length=50))
    location = serializers.CharField(max_length=100)
    reviews = serializers.IntegerField(default=0)
    rating = serializers.FloatField(min_value=0, max_value=5, default=0)
    images = serializers.ListField(child=serializers.CharField())  # Allow storing file paths like "/pic1.jpg"
    description = serializers.CharField(max_length=500, allow_blank=True, required=False)

    # Timestamps
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate_availability(self, value):
        """Ensure availability follows YYYY-MM-DD format."""
        try:
            datetime.datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise serializers.ValidationError("Availability must be in 'YYYY-MM-DD' format.")
        return value

    def validate_tags(self, value):
        """Ensure tags contain 1 or 2 values from the allowed list."""
        allowed_tags = ["Wedding", "Portrait", "Wildlife", "Videography"]
        if not (1 <= len(value) <= 2):
            raise serializers.ValidationError("Tags must contain 1 or 2 values.")
        for tag in value:
            if tag not in allowed_tags:
                raise serializers.ValidationError(f"Invalid tag: {tag}. Allowed tags: {allowed_tags}")
        return value

    def validate_images(self, value):
        """Ensure all images are in .jpg format."""
        for img in value:
            if not img.endswith(".jpg"):
                raise serializers.ValidationError(f"Invalid image format: {img}. Only '.jpg' is allowed.")
        return value

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

        