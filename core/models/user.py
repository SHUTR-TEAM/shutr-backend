from mongoengine import Document, StringField, FloatField, IntField, DateTimeField, ListField, URLField, EmailField
import datetime

class User(Document):
    # Personal Information
    first_name = StringField(max_length=50, required=True)
    last_name = StringField(max_length=50, required=True)
    email = EmailField(unique=True, required=True)
    password = StringField(max_length=255, required=True)  # Ensure to hash passwords
    nic = StringField(max_length=50, required=True)  # Assuming NIC is required
    phone_num = StringField(max_length=50, required=True)
    address = StringField(max_length=255, required=False)  # Address is optional
    profile_image_url = StringField(max_length=255, required=False)

    # Business/Photographer Details
    name = StringField(max_length=100, required=True)  # Business name or display name
    price = FloatField(required=True)
    min_price = FloatField(required=True)
    max_price = FloatField(required=True)
    availability = StringField(required=True)  # Changed to StringField to match YYYY-MM-DD format
    experience_level = StringField(choices=["Beginner", "Intermediate", "Expert"], required=True)
    tags = ListField(StringField(max_length=50), required=True)  # List of tags
    location = StringField(max_length=100, required=True)
    reviews = IntField(default=0)
    rating = FloatField(min_value=0, max_value=5, default=0)
    images = ListField(StringField(), required=True)  # Changed from URLField to allow file paths like "/pic1.jpg"
    description = StringField(max_length=500, required=False)

    # Timestamps
    created_at = DateTimeField(default=lambda: datetime.datetime.utcnow())
    updated_at = DateTimeField(default=lambda: datetime.datetime.utcnow())

    meta = {
        'collection': 'users',  # MongoDB collection name
        'indexes': [
            {'fields': ['email'], 'unique': True},  # Ensure email uniqueness
            {'fields': ['name']},  # Index for faster searches
            {'fields': ['location']},  # Index for location-based searches
        ],
    }

    