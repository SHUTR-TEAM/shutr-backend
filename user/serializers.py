from rest_framework import serializers

from portfolio.serializers import HeaderSerializer
from .models import User, Photographer

class UserSerializer(serializers.Serializer):
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
    portfolio = HeaderSerializer()
    verified = serializers.BooleanField(default=False)

    def create(self, validated_data):
        user = Photographer(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user