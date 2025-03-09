from rest_framework import serializers
from .models import booking_information

class booking_informationSerializer(serializers.ModelSerializer):
    class Meta:
        model = booking_information  # Fixed reference to correct model
        fields = '__all__'
