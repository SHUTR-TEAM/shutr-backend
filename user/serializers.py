from bson import ObjectId
from rest_framework import serializers

from portfolio.models import Header
# from django.utils.module_loading import import_string

# from portfolio.serializers import HeaderSerializer
from .models import User, Photographer


# def get_header_serializer():
#     return import_string('portfolio.serializers.HeaderSerializer')

class ObjectIdField(serializers.Field):
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        if not ObjectId.is_valid(data):
            raise serializers.ValidationError("Invalid ObjectId")
        return ObjectId(data)

class UserSerializer(serializers.Serializer):
    id = ObjectIdField(read_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    nic = serializers.CharField(max_length=50, required=True)
    phone_num = serializers.CharField(max_length=50, required=True)
    address = serializers.CharField(max_length=255, required=False)
    profile_image_url = serializers.CharField(max_length=255, required=False)

    role = serializers.ChoiceField(choices=["user", "photographer"], default="user")
    is_active = serializers.BooleanField(default=True)

    google_access_token= serializers.CharField(max_length=255, required=False)
    refresh_token = serializers.CharField(max_length=255, required=False)
    google_token_expiry = serializers.CharField(max_length=255, required=False)

    def create(self, validated_data):
        role = validated_data.pop("role", "user")

        if role == "photographer":
            user = Photographer(**validated_data)
        else:
            user = User(**validated_data)

        user.set_password(validated_data["password"])
        user.save()
        return user


class PhotographerSerializer(UserSerializer):
    portfolio = serializers.SerializerMethodField(read_only=True)
    verified = serializers.BooleanField(default=False)

    def create(self, validated_data):
        user = Photographer(**validated_data)
        user.set_password(validated_data["password"])
        saved_user = user.save()

        portfolio = Header.objects.create(photographer=saved_user)
        saved_user.portfolio = portfolio

        return saved_user
    
    def get_portfolio(self, obj):
        from portfolio.serializers import HeaderSerializer
        try:
            portfolio = Header.objects.get(photographer=obj)
            return HeaderSerializer(portfolio, context=self.context).data
        except Header.DoesNotExist:
            return None


class PhotographerMinimalSerializer(UserSerializer):
    verified = serializers.BooleanField(default=False)