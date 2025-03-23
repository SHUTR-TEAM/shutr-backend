from rest_framework import serializers
from bson import ObjectId

from user.models import Photographer, User
from user.serializers import PhotographerMinimalSerializer, PhotographerSerializer, UserSerializer
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
    description = serializers.CharField(max_length=1000, allow_blank=True, required=False)

    photographer_id = serializers.CharField(write_only=True)
    photographer = serializers.SerializerMethodField(read_only=True)

    Background_image_url = serializers.SerializerMethodField()
    profile_image_url = serializers.SerializerMethodField()

    images = serializers.SerializerMethodField()
    social_links = serializers.SerializerMethodField()
    packages = serializers.SerializerMethodField()

    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    max_price = serializers.SerializerMethodField()

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
        """Create and return a new Package instance."""
        photographer_id = validated_data.pop('photographer_id')
        photographer = Photographer.objects(id=photographer_id).first()

        if not photographer:
            raise serializers.ValidationError("User or Photographer not found")

        portfolio = Header.objects.create(photographer=photographer, **validated_data)

        social_links = SocialLinks.objects.create(portfolio=portfolio)
        portfolio.social_links = social_links
        
        return portfolio

    def update(self, instance, validated_data):
        """Update and return an existing header instance."""
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.updated_at = datetime.datetime.utcnow()
        instance.save()
        return instance

    def get_images(self, obj):
        """Retrieve related galleries based on portfolioID."""
        galleries = Gallery.objects.filter(portfolioID=str(obj.id))  # Ensure matching ID format
        return GallerySerializer(galleries, many=True).data
    
    def get_photographer(self, obj):
        """Fetch the photographer for the portfolio."""
        if obj.photographer:
            return PhotographerMinimalSerializer(obj.photographer, context=self.context).data

    def get_social_links(self, obj):
        """Retrieve social links for this portfolio."""
        social_links = SocialLinks.objects.filter(portfolio=obj).first()
        if social_links:
            return {
                'facebook': social_links.facebook,
                'instagram': social_links.instagram,
                'twitter': social_links.twitter,
                'linkedin': social_links.linkedin
            }
        return None

    def get_packages(self, obj):
        """Retrieve packages for this portfolio."""
        packages = Package.objects.filter(portfolio=obj)
        return PackageSerializer(packages, many=True, context=self.context).data

    def get_reviews(self, obj):
        """Get the total number of reviews for this photographer."""
        # Assuming reviews are associated with the photographer linked to this portfolio
        if obj.photographer:
            return Review.objects.filter(photographer=obj.photographer).count()
        return 0

    def get_rating(self, obj):
        """Calculate the average rating for this photographer."""
        if obj.photographer:
            reviews = Review.objects.filter(photographer=obj.photographer)
            if reviews:
                total_rating = sum(review.rating for review in reviews)
                return round(total_rating / reviews.count(), 1)  # Return as float with 1 decimal place
        return 0.0

    def get_min_price(self, obj):
        """Get the minimum price from all packages."""
        packages = Package.objects.filter(portfolio=obj)
        if packages:
            # Convert price strings to numbers, handling any formatting
            prices = []
            for package in packages:
                try:
                    # Remove any non-numeric characters except decimal point
                    price_str = ''.join(c for c in package.price if c.isdigit() or c == '.')
                    prices.append(float(price_str))
                except (ValueError, TypeError):
                    continue
            
            return min(prices) if prices else None
        return None

    def get_max_price(self, obj):
        """Get the maximum price from all packages."""
        packages = Package.objects.filter(portfolio=obj)
        if packages:
            # Convert price strings to numbers, handling any formatting
            prices = []
            for package in packages:
                try:
                    # Remove any non-numeric characters except decimal point
                    price_str = ''.join(c for c in package.price if c.isdigit() or c == '.')
                    prices.append(float(price_str))
                except (ValueError, TypeError):
                    continue
            
            return max(prices) if prices else None
        return None


class ReviewSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)  # MongoDB ObjectId as string
    
    user_id = serializers.CharField(write_only=True)  
    user = UserSerializer(read_only=True)

    photographer_id = serializers.CharField(write_only=True)
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
        photographer = Photographer.objects(id=photographer_id).first()

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
            photographer = Photographer.objects(id=validated_data.pop('photographerID')).first()
            if not photographer:
                raise serializers.ValidationError("Photographer not found")
            instance.photographer = photographer

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance


class PackageSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)  # MongoDB ObjectId as string
    
    # userID = serializers.CharField(write_only=True)
    # user = UserSerializer(read_only=True)

    portfolio_id = serializers.CharField(write_only=True)
    portfolio = serializers.SerializerMethodField(read_only=True)

    title = serializers.CharField(max_length=255)
    price = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=1000)
    details = serializers.ListField(child=serializers.CharField())

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate_portfolio_id(self, value):
        """Validate and convert portfolio_id from string to ObjectId."""
        if not ObjectId.is_valid(value):
            raise serializers.ValidationError("Invalid ObjectId for portfolio_id")
        return ObjectId(value)

    def create(self, validated_data):
        """Create and return a new Package instance."""
        portfolio_id = validated_data.pop('portfolio_id')
        portfolio = Header.objects(id=portfolio_id).first()

        if not portfolio:
            raise serializers.ValidationError("Portfolio not found")

        package = Package.objects.create(portfolio=portfolio, **validated_data)
        return package

    def update(self, instance, validated_data):
        """Update and return an existing Package instance."""
        if 'portfolio_id' in validated_data:
            portfolio = Header.objects(id=validated_data.pop('portfolio_id')).first()
            if not portfolio:
                raise serializers.ValidationError("Portfolio not found")
            instance.portfolio = portfolio

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.updated_at = datetime.datetime.utcnow()
        instance.save()
        return instance


class SocialLinksSerializer(serializers.Serializer):
    """Serializer for the SocialLinks model."""

    id = ObjectIdField(read_only=True)  # MongoDB ObjectId
    # userID = serializers.CharField(write_only=True)  # Accept only user ID when creating/updating
    # user = UserSerializer(read_only=True)  # Return full user object when retrieving

    portfolio_id = serializers.CharField(write_only=True)
    portfolio = serializers.SerializerMethodField(read_only=True)
    
    facebook = serializers.URLField(required=False, allow_blank=True)
    instagram = serializers.URLField(required=False, allow_blank=True)
    twitter = serializers.URLField(required=False, allow_blank=True)
    linkedin = serializers.URLField(required=False, allow_blank=True)

    def validate_portfolio_id(self, value):
        """Validate and convert portfolio_id from string to ObjectId."""
        if not ObjectId.is_valid(value):
            raise serializers.ValidationError("Invalid ObjectId for portfolio_id")
        return ObjectId(value)

    def create(self, validated_data):
        """Create and return a new SocialLinks instance."""
        portfolio_id = validated_data.pop('portfolio_id')
        portfolio = Header.objects(id=portfolio_id).first()

        if not portfolio:
            raise serializers.ValidationError("Portfolio not found")

        social_links = SocialLinks.objects.create(portfolio=portfolio, **validated_data)
        return social_links

    def update(self, instance, validated_data):
        """Update and return an existing SocialLinks instance."""
        if 'portfolio_id' in validated_data:
            portfolio = Header.objects(id=validated_data.pop('portfolio_id')).first()
            if not portfolio:
                raise serializers.ValidationError("Portfolio not found")
            instance.portfolio = portfolio

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance