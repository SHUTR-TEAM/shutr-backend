from rest_framework import serializers
from .models import BookingInformation

class BookingInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
