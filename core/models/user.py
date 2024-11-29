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

from mongoengine import Document, StringField, EmailField, DateTimeField
import datetime

class User(Document):
    first_name = StringField(max_length=50, required=True)
    last_name = StringField(max_length=50, required=True)
    email = EmailField(unique=True, required=True)
    password = StringField(max_length=50, required=True)  # Ensure to hash passwords
    nic = StringField(max_length=50, required=True)  # Assuming NIC is required
    phone_num = StringField(max_length=50, required=True)
    address = StringField(max_length=50, required=False)  # Assuming address is optional
    profile_image_url = StringField(max_length=255, required=False)
    created_at = DateTimeField(default=lambda: datetime.datetime.utcnow())  # Auto set current time
    updated_at = DateTimeField(default=lambda: datetime.datetime.utcnow())  # Set manually on updates

    meta = {
        'collection': 'users',  # Specify MongoDB collection name
        'indexes': [
            {'fields': ['email'], 'unique': True},  # Create an index on email
        ],
    }
