







# ###

from rest_framework import serializers
from bson import ObjectId

from user.models import User
from user.serializers import UserSerializer
from .models import Header, Gallery, Package, Review, SocialLinks
import datetime

from rest_framework import serializers
from bson import ObjectId

from django.conf import settings
from urllib.parse import urljoin

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




class GallerySerializer(serializers.Serializer):
    portfolioID = serializers.CharField()
    photographerID = serializers.CharField(write_only=True)
    url = serializers.CharField() 
    category = serializers.CharField(max_length=20)

    # Return full photographer objects when retrieving
    photographer = UserSerializer(read_only=True)

    def validate_photographerID(self, value):
        """Validate and convert photographerID from string to ObjectId"""
        if not ObjectId.is_valid(value):
            raise serializers.ValidationError("Invalid ObjectId for photographerID")
        return ObjectId(value)
   
    def create(self, validated_data):
        """Create and return a new Gallery instance."""
        photographer_id = validated_data.pop('photographerID')
        photographer = User.objects(id=photographer_id).first()
        
        if not photographer:
            raise serializers.ValidationError("Photographer not found")

        gallery = Gallery.objects.create(photographer=photographer, **validated_data)
        return gallery    

    def update(self, instance, validated_data):
        """Update and return an existing Gallery instance."""
        if 'photographerID' in validated_data:
            photographer = User.objects(id=validated_data.pop('photographerID')).first()
            if not photographer:
                raise serializers.ValidationError("Photographer not found")
            instance.photographer = photographer
        
        for key, value in validated_data.items():
            setattr(instance, key, value)
        
        instance.save()
        return instance
    

class HeaderSerializer(serializers.Serializer): 
    """Custom serializer for the Header model."""
    
    id = ObjectIdField(read_only=True)  # MongoDB ObjectId
    name = serializers.CharField(max_length=41)
    # Background_image_url = serializers.CharField(max_length=255, allow_blank=True, required=False)
    # profile_image_url = serializers.CharField(max_length=255, allow_blank=True, required=False)
    Background_image_url = serializers.SerializerMethodField()
    profile_image_url = serializers.SerializerMethodField()
    # images = GallerySerializer(many=True, read_only=True, source="*")
    images = serializers.SerializerMethodField()


    description = serializers.CharField(max_length=1000, allow_blank=True, required=False)

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def get_Background_image_url(self, obj):
        return self.get_full_media_url(obj.Background_image_url)

    def get_profile_image_url(self, obj):
        return self.get_full_media_url(obj.profile_image_url)

    def get_full_media_url(self, media_path):
        """Ensure media URLs are fully qualified."""
        request = self.context.get("request")
        if media_path:
            return request.build_absolute_uri(media_path) if request else urljoin(settings.MEDIA_URL, media_path)
        return None


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

    def get_images(self, obj):
        # return Gallery.objects(portfolioID=obj)
        # //print("===============================")
        # galleries = Gallery.objects.filter(portfolioID=str(obj.id))  # Ensure matching ID format
        # //return []
        """Retrieve related galleries based on portfolioID."""
        galleries = Gallery.objects.filter(portfolioID=str(obj.id))  # Ensure matching ID format
        return GallerySerializer(galleries, many=True).data



class ReviewSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)  # MongoDB ObjectId as string
    
    # Accept only user IDs when creating/updating
    userID = serializers.CharField(write_only=True)  
    photographerID = serializers.CharField(write_only=True)
    
    # Return full user objects when retrieving
    user = UserSerializer(read_only=True)
    photographer = UserSerializer(read_only=True)
    
    rating = serializers.FloatField(min_value=0.0, max_value=10.0)
    reviewText = serializers.CharField(max_length=1000)



    def validate_userID(self, value):
        """Validate and convert userID from string to ObjectId"""
        if not ObjectId.is_valid(value):
            raise serializers.ValidationError("Invalid ObjectId for userID")
        return ObjectId(value)  # Convert string to ObjectId

    def validate_photographerID(self, value):
        """Validate and convert photographerID from string to ObjectId"""
        if not ObjectId.is_valid(value):
            raise serializers.ValidationError("Invalid ObjectId for photographerID")
        return ObjectId(value)  # Convert string to ObjectId

    def create(self, validated_data):
        """Create and return a new Review instance."""
        user_id = validated_data.pop('userID')
        photographer_id = validated_data.pop('photographerID')

        # Fetch User objects
        user = User.objects(id=user_id).first()
        photographer = User.objects(id=photographer_id).first()

        if not user or not photographer:
            raise serializers.ValidationError("User or Photographer not found")

        review = Review.objects.create(user=user, photographer=photographer, **validated_data)
        return review

    def update(self, instance, validated_data):
        """Update and return an existing Review instance."""
        if 'userID' in validated_data:
            user = User.objects(id=validated_data.pop('userID')).first()
            if not user:
                raise serializers.ValidationError("User not found")
            instance.user = user
        
        if 'photographerID' in validated_data:
            photographer = User.objects(id=validated_data.pop('photographerID')).first()
            if not photographer:
                raise serializers.ValidationError("Photographer not found")
            instance.photographer = photographer

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance


# class PackageSerializer(serializers.Serializer):
#     id = ObjectIdField(read_only=True)
#     title = serializers.CharField(max_length=255)
#     price = serializers.CharField(max_length=50)
#     description = serializers.CharField(max_length=1000)
#     details = serializers.ListField(child=serializers.CharField())
#     created_at = serializers.DateTimeField(read_only=True)
#     updated_at = serializers.DateTimeField(read_only=True)

#     def create(self, validated_data):
#         return Package(**validated_data).save()

#     def update(self, instance, validated_data):
#         for key, value in validated_data.items():
#             setattr(instance, key, value)
            
#         instance.updated_at = datetime.datetime.utcnow()
#         instance.save()
#         return instance


# class PackageSerializer(serializers.Serializer):
#     id = serializers.CharField(read_only=True)  # MongoDB ObjectId as string
    
#     # Accept only user ID when creating/updating
#     userID = serializers.CharField(write_only=True)

#     # Return full user object when retrieving
#     user = UserSerializer(read_only=True)
    
#     title = serializers.CharField(max_length=255)
#     price = serializers.CharField(max_length=50)
#     description = serializers.CharField(max_length=1000)
#     details = serializers.ListField(child=serializers.CharField())

#     created_at = serializers.DateTimeField(read_only=True)
#     updated_at = serializers.DateTimeField(read_only=True)

#     def validate_userID(self, value):
#         """Validate and convert userID from string to ObjectId"""
#         if not ObjectId.is_valid(value):
#             raise serializers.ValidationError("Invalid ObjectId for userID")
#         return ObjectId(value)  # Convert string to ObjectId

#     def create(self, validated_data):
#         """Create and return a new Package instance."""
#         user_id = validated_data.pop('userID')

#         # Fetch User object
#         user = User.objects(id=user_id).first()
#         if not user:
#             raise serializers.ValidationError("User not found")

#         package = Package.objects.create(user=user, **validated_data)
#         return package

#     def update(self, instance, validated_data):
#         """Update and return an existing Package instance."""
#         if 'userID' in validated_data:
#             user = User.objects(id=validated_data.pop('userID')).first()
#             if not user:
#                 raise serializers.ValidationError("User not found")
#             instance.user = user

#         for key, value in validated_data.items():
#             setattr(instance, key, value)

#         instance.updated_at = datetime.datetime.utcnow()
#         instance.save()
#         return instance


class PackageSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)  # MongoDB ObjectId as string
    
    # Accept only user ID when creating/updating
    userID = serializers.CharField(write_only=True)

    # Return full user object when retrieving
    user = UserSerializer(read_only=True)
    
    title = serializers.CharField(max_length=255)
    price = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=1000)
    details = serializers.ListField(child=serializers.CharField())

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate_userID(self, value):
        """Validate and convert userID from string to ObjectId"""
        if not ObjectId.is_valid(value):
            raise serializers.ValidationError("Invalid ObjectId for userID")
        # return ObjectId(value)  # Convert string to ObjectId

        user = User.objects(id=value).first()  # Fetch user
        if not user:
            raise serializers.ValidationError("User not found")

        return user  

    def create(self, validated_data):
        """Create and return a new Package instance."""
        user = validated_data.pop('userID')

        # Fetch User document instead of passing ObjectId
        # user = User.objects(id=user_id).first()
        # if not user:
        #     raise serializers.ValidationError("User not found")

        # Create the package with the User document
        package = Package.objects.create(user=user, **validated_data)
        return package

    def update(self, instance, validated_data):
        """Update and return an existing Package instance."""
        if 'userID' in validated_data:
            user = User.objects(id=validated_data.pop('userID')).first()
            if not user:
                raise serializers.ValidationError("User not found")
            instance.user = user  # Assign User document, not ObjectId

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.updated_at = datetime.datetime.utcnow()
        instance.save()
        return instance




class SocialLinksSerializer(serializers.Serializer):
    """Serializer for the SocialLinks model."""

    # id = ObjectIdField(read_only=True)  # MongoDB ObjectId
    userID = serializers.CharField(write_only=True)  # Accept only user ID when creating/updating
    user = UserSerializer(read_only=True)  # Return full user object when retrieving
    
    facebook = serializers.URLField(required=False, allow_blank=True)
    instagram = serializers.URLField(required=False, allow_blank=True)
    twitter = serializers.URLField(required=False, allow_blank=True)
    linkedin = serializers.URLField(required=False, allow_blank=True)

    def validate_userID(self, value):
        """Validate and convert userID from string to ObjectId."""
        if not ObjectId.is_valid(value):
            raise serializers.ValidationError("Invalid ObjectId for userID")
        return ObjectId(value)

    def create(self, validated_data):
        """Create and return a new SocialLinks instance."""
        user_id = validated_data.pop('userID')
        user = User.objects(id=user_id).first()

        if not user:
            raise serializers.ValidationError("User not found")

        social_links = SocialLinks.objects.create(user=user, **validated_data)
        return social_links

    def update(self, instance, validated_data):
        """Update and return an existing SocialLinks instance."""
        if 'userID' in validated_data:
            user = User.objects(id=validated_data.pop('userID')).first()
            if not user:
                raise serializers.ValidationError("User not found")
            instance.user = user

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance
