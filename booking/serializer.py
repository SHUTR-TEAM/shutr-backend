from rest_framework import serializers
from bson import ObjectId
from core.models import Booking  # Import your MongoEngine model
import datetime

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
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    alternative_contact = serializers.CharField(max_length=20, required=False, allow_blank=True)


# Serializer for Venue
class VenueSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=255)
    indoor = serializers.BooleanField(default=True)
    notes = serializers.CharField(max_length=255, required=False, allow_blank=True)


# Serializer for Event
class EventSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    type = serializers.CharField(max_length=100)
    date = serializers.DateTimeField()
    duration_start = serializers.CharField(max_length=10)
    duration_end = serializers.CharField(max_length=10)
    venue = VenueSerializer()
    expected_guests = serializers.IntegerField(default=0)


# Serializer for PhotographyDetails
class PhotographyDetailsSerializer(serializers.Serializer):
    style = serializers.ListField(child=serializers.CharField(max_length=50), required=False)
    specific_shots = serializers.ListField(child=serializers.CharField(max_length=100), required=False)
    special_instructions = serializers.CharField(max_length=255, required=False, allow_blank=True)
    editing_preferences = serializers.CharField(max_length=100, required=False, allow_blank=True)


# Serializer for Package
class PackageSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    num_photographers = serializers.IntegerField(default=1)
    extra_services = serializers.ListField(child=serializers.CharField(max_length=100), required=False)
    price = serializers.FloatField()
    currency = serializers.CharField(max_length=10, default="USD")


# Serializer for Deliverables
class DeliverablesSerializer(serializers.Serializer):
    format = serializers.ListField(child=serializers.CharField(max_length=50), default=["Digital Album"])
    expected_delivery_date = serializers.DateTimeField()


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
    client = ClientSerializer()
    event = EventSerializer()
    photography_details = PhotographyDetailsSerializer(required=False)
    package = PackageSerializer()
    deliverables = DeliverablesSerializer()
    payment = PaymentSerializer()
    status = serializers.CharField(max_length=50, default="Pending")
    cancellation_policy_agreed = serializers.BooleanField(default=False)
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
