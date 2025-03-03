from mongoengine import Document, StringField, EmailField, DateTimeField, BooleanField, IntField, FloatField, ListField, EmbeddedDocument, EmbeddedDocumentField
import datetime


# Client Details
class Client(EmbeddedDocument):
    first_name = StringField(max_length=100, required=True)
    last_name = StringField(max_length=100, required=True)
    phone = StringField(max_length=20, required=True)
    email = EmailField(required=True)
    address = StringField(max_length=100, required=False)
    nic = StringField(max_length=20, required=True)


# Venue Details
class Venue(EmbeddedDocument):
    address = StringField(max_length=255, required=True)
    event_setting = StringField(max_length=255, required=True)
    # notes = StringField(max_length=255, required=False)


# Event Details
class Event(EmbeddedDocument):
    # name = StringField(max_length=255, required=True)
    type = StringField(max_length=100, required=True)
    date = DateTimeField(required=True)
    # duration_start = StringField(max_length=10, required=True)  # Example: "14:00"
    # duration_end = StringField(max_length=10, required=True)  # Example: "20:00"
    venue = EmbeddedDocumentField(Venue)
    guest_count = IntField(default=0)


# Photography Preferences
# class PhotographyDetails(EmbeddedDocument):
#     style = ListField(StringField(max_length=50), default=[])  # ["Candid", "Traditional"]
#     specific_shots = ListField(StringField(max_length=100), default=[])  # ["First Dance", "Family Portrait"]
#     special_instructions = StringField(max_length=255, required=False)
#     editing_preferences = StringField(max_length=100, required=False)


# Package Selection
class Package(EmbeddedDocument):
    name = StringField(max_length=100, required=True)
    num_photographers = IntField(default=1)
    extra_services = ListField(StringField(max_length=100), default=[])  # ["Drone Shots", "Videography"]
    price = FloatField(required=True)
    currency = StringField(max_length=10, default="USD")


# Deliverables
# class Deliverables(EmbeddedDocument):
#     format = ListField(StringField(max_length=50), default=["Digital Album"])  # ["USB Drive", "Prints"]
#     expected_delivery_date = DateTimeField(required=True)


# Payment Information
class Payment(EmbeddedDocument):
    deposit_paid = BooleanField(default=False)
    total_amount = FloatField(required=True)
    amount_paid = FloatField(default=0.0)
    balance_due = FloatField(default=0.0)
    payment_status = StringField(max_length=50, default="Pending")  # ["Pending", "Paid", "Overdue"]


# Booking Model
class Booking(Document):
    client = EmbeddedDocumentField(Client, required=True)
    event = EmbeddedDocumentField(Event, required=True)
    # photography_details = EmbeddedDocumentField(PhotographyDetails, required=False)
    package = EmbeddedDocumentField(Package, required=True)
    # deliverables = EmbeddedDocumentField(Deliverables, required=True)
    payment = EmbeddedDocumentField(Payment, required=True)
    status = StringField(max_length=50, default="Pending")  # ["Pending", "Confirmed", "Cancelled"]
    additional_notes = StringField(max_length=512) 
    cancellation_policy_agreed = BooleanField(default=False)
    terms_and_conditions_agreed = BooleanField(default=False)
    created_at = DateTimeField(default=lambda: datetime.datetime.utcnow())  # Auto-set on creation
    updated_at = DateTimeField(default=lambda: datetime.datetime.utcnow())  # Manually update on changes

    meta = {
        'collection': 'bookings',  # MongoDB collection name
        'indexes': [
            {'fields': ['event.date']},  # Index on event date for efficient queries
        ],
    }

    def __str__(self):
        return f"Booking for {self.client.name} on {self.event.date}"
