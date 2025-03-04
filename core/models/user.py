# from django.db import models

# class User(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=50)
#     nic = models.CharField(max_length=50)
#     phone_num = models.CharField(max_length=50)
#     address = models.CharField(max_length=50)
#     profile_image_url = models.CharField(max_length=50)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

from mongoengine import Document, StringField, FloatField, IntField, DateTimeField, ListField, URLField
import datetime

class User(Document):
    _id = StringField(primary_key=True, required=True)  # UUID as string
    name = StringField(max_length=100, required=True)
    price = FloatField(required=True)
    min_price = FloatField(required=True)
    max_price = FloatField(required=True)
    availability = DateTimeField(required=True)
    experience_level = StringField(choices=["Beginner", "Intermediate", "Expert"], required=True)
    tags = ListField(StringField(max_length=50))  # List of tags like "Event", "Portrait", "Fashion"
    location = StringField(max_length=100, required=True)
    reviews = IntField(default=0)
    rating = FloatField(min_value=0, max_value=5, default=0)
    images = ListField(URLField())  # List of image URLs
    description = StringField(max_length=500)
    
    created_at = DateTimeField(default=lambda: datetime.datetime.utcnow())
    updated_at = DateTimeField(default=lambda: datetime.datetime.utcnow())

    meta = {
        'collection': 'users',  # MongoDB collection name
        'indexes': [
            {'fields': ['name']},
            {'fields': ['location']},
        ],
    }
