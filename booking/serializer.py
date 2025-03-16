from rest_framework import serializers
from bson import ObjectId
import datetime

from booking.models.booking import Booking
from portfolio.serializers import PackageSerializer

# Custom field to handle MongoDB ObjectId serialization
class ObjectIdField(serializers.Field):
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        if not ObjectId.is_valid(data):
            raise serializers.ValidationError("Invalid ObjectId")
        return ObjectId(data)


# Serializer for Client
class ClientSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    address = serializers.CharField(max_length=100, required=False)
    nic = serializers.CharField(max_length=20)


# Serializer for Event
class EventSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=255)
    date = serializers.CharField(max_length=255)
    event_setting = serializers.CharField(max_length=255)
    guest_count = serializers.IntegerField(default=0)
    type = serializers.CharField(max_length=100)


# Serializer for Payment
class PaymentSerializer(serializers.Serializer):
    deposit_paid = serializers.BooleanField(default=False)
    total_amount = serializers.FloatField()
    amount_paid = serializers.FloatField(default=0.0)
    balance_due = serializers.FloatField(default=0.0)
    payment_status = serializers.CharField(max_length=50, default="Pending")


# **Main Booking Serializer**
class BookingSerializer(serializers.Serializer):
    id = ObjectIdField(read_only=True)
    photographer_id = serializers.CharField(max_length=128) 
    client_id = serializers.CharField(max_length=128) 
    client = ClientSerializer()
    event = EventSerializer()
    package_id = serializers.CharField(max_length=128) 
    # package = PackageSerializer(required=False, allow_null=True)
    payment = PaymentSerializer(required=False)
    status = serializers.CharField(max_length=50, default="Pending")
    additional_notes = serializers.CharField(max_length=512, required=False, allow_blank=True) 
    cancellation_policy_agreed = serializers.BooleanField(default=False)
    terms_and_conditions_agreed = serializers.BooleanField(default=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        """Create and return a new Booking instance."""
        return Booking(**validated_data).save()

    def update(self, instance, validated_data):
        """Update and return an existing Booking instance."""
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.updated_at = datetime.datetime.utcnow()
        instance.save()
        return instance
