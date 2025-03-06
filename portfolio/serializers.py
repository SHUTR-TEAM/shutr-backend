from rest_framework import serializers
from bson import ObjectId
from .models import Header, Gallery, Review, ReviewFormat, GalleryFormat  # Import your MongoEngine model
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



# class GallerySerializer(serializers.Serializer):
#        """Custom serializer for the Gallery model."""
      
#        id = ObjectIdField(read_only=True)
#        photo_collection = serializers.ListField(child=serializers.URLField())

#        def create(self, validated_data):
#         """Create and return a new gallery instance."""
#         return Gallery(**validated_data).save()

#        def update(self, instance, validated_data):
#             """Update and return an existing gallery instance."""
#             for key, value in validated_data.items():
#                 setattr(instance, key, value)
#             #instance.updated_at = datetime.datetime.utcnow()
#             instance.save()
#             return instance


class GalleryFormatSerializer(serializers.Serializer):
    url = serializers.URLField()
    catagory = serializers.CharField(max_length=20)


class GallerySerializer(serializers.Serializer):
    id = ObjectIdField(read_only=True)
    Gallery = GalleryFormatSerializer(many=True)  # Nested serializer for multiple reviews


    def create(self, validated_data):
        """Create and return a new Gallery instance."""
        gallery_data = validated_data.pop('Gallery', [])
        gallery_instances = [GalleryFormat(**gallery) for gallery in gallery_data]
        return Gallery(Gallery=gallery_instances).save()

    def update(self, instance, validated_data):
        """Update and return an existing Gallery instance."""
        if "Gallery" in validated_data:
            gallery_data = validated_data.pop("Gallery")
            instance.Gallery = [GalleryFormat(**gallery) for gallery in gallery_data]
        
        for key, value in validated_data.items():
            setattr(instance, key, value)
        
        instance.save()
        return instance


# class ReviewSerializer(serializers.Serializer):      
#      id = ObjectIdField(read_only=True)  
#      name = serializers.CharField(max_length=41)
#      rating = serializers.FloatField(min_value=0.0, max_value=10.0)
#      reviewText = serializers.CharField(max_length=1000)
#      profile_image_url = serializers.CharField(max_length=255)


#      def create(self, validated_data):
#         """Create and return a new review instance."""
#         return Review(**validated_data).save()

#      def update(self, instance, validated_data):
#             """Update and return an existing review instance."""
#             for key, value in validated_data.items():
#                 setattr(instance, key, value)
#             #instance.updated_at = datetime.datetime.utcnow()
#             instance.save()
#             return instance


class ReviewFormatSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=41)
    rating = serializers.FloatField(min_value=0.0, max_value=10.0)
    reviewText = serializers.CharField(max_length=1000)
    profile_image_url = serializers.CharField(max_length=255)
    address = serializers.CharField(max_length=35)


class ReviewSerializer(serializers.Serializer):
    id = ObjectIdField(read_only=True)
    reviews = ReviewFormatSerializer(many=True)  # Nested serializer for multiple reviews

    def create(self, validated_data):
        """Create and return a new Review instance."""
        reviews_data = validated_data.pop('reviews', [])
        review_instances = [ReviewFormat(**review) for review in reviews_data]
        return Review(reviews=review_instances).save()

    def update(self, instance, validated_data):
        """Update and return an existing Review instance."""
        if "reviews" in validated_data:
            reviews_data = validated_data.pop("reviews")
            instance.reviews = [ReviewFormat(**review) for review in reviews_data]
        
        for key, value in validated_data.items():
            setattr(instance, key, value)
        
        instance.save()
        return instance

<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
# class PackageSerializer(serializers.Serializer):
#     id = ObjectIdField(read_only=True)
#     title = serializers.CharField(max_length=255)
#     price = serializers.CharField(max_length=50)
#     description = serializers.CharField(max_length=1000)
#     details = serializers.ListField(child=serializers.CharField())
#     package_type = serializers.CharField(max_length=100)
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

class PackageSerializer(serializers.ModelSerializer):
    """Serializer for the Package model."""
    
    class Meta:
        model = Package
        fields = ['id', 'title', 'price', 'description', 'details', 'package_type']
<<<<<<< Updated upstream
        read_only_fields = ['id']
>>>>>>> Stashed changes
=======
        read_only_fields = ['id']
>>>>>>> Stashed changes
