from rest_framework import serializers
from .models import Photographer
from django.contrib.auth.hashers import make_password

class PhotographerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photographer
        fields = ['email', 'name', 'password', 'username', 'id_number', 'bank_account', 'id_verification']

    def create(self, validated_data):
        # Hash the password before saving
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)