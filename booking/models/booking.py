from mongoengine import Document, StringField, EmailField, DateTimeField, BooleanField, IntField, FloatField, ListField, EmbeddedDocument, EmbeddedDocumentField, ReferenceField
import datetime

from portfolio.models import Package


# Client Details
class Client(EmbeddedDocument):
    address = StringField(max_length=100, required=False)
    email = EmailField(required=True)
    first_name = StringField(max_length=100, required=True)
    last_name = StringField(max_length=100, required=True)
    nic = StringField(max_length=20, required=True)
    phone = StringField(max_length=20, required=True)

# Event Details
class Event(EmbeddedDocument):
    address = StringField(max_length=255, required=True)
    date = StringField(max_length=255, required=True)
    event_setting = StringField(max_length=255, required=True)
    guest_count = IntField(default=0)
    type = StringField(max_length=100, required=True)


# Payment Information
class Payment(EmbeddedDocument):
    deposit_paid = BooleanField(default=False)
    total_amount = FloatField(required=True)
    amount_paid = FloatField(default=0.0)
    balance_due = FloatField(default=0.0)
    payment_status = StringField(max_length=50, default="Pending")  # ["Pending", "Paid", "Overdue"]


# Booking Model
class Booking(Document):
    photographer_id = ReferenceField('User', required=True)
    client_id = ReferenceField('User', required=True)
    client = EmbeddedDocumentField(Client, required=True)
    event = EmbeddedDocumentField(Event, required=True)
    package_id = ReferenceField('Package', required=False)
    # package = EmbeddedDocumentField(Package, required=False, allow_null=True)
    payment = EmbeddedDocumentField(Payment, required=False)
    status = StringField(max_length=50, default="Pending")  # ["Pending", "Confirmed", "Cancelled"]
    additional_notes = StringField(max_length=512) 
    cancellation_policy_agreed = BooleanField(default=False)
    terms_and_conditions_agreed = BooleanField(default=False)
    created_at = DateTimeField(default=lambda: datetime.datetime.utcnow())  # Auto-set on creation
    updated_at = DateTimeField(default=lambda: datetime.datetime.utcnow())  # Manually update on changes

    meta = {
        'collection': 'bookings',  # MongoDB collection name
        # 'indexes': [
        #     {'fields': ['event.date']},  # Index on event date for efficient queries
        # ],
    }

    def __str__(self):
        return f"Booking for {self.client.name} on {self.event.date}"
