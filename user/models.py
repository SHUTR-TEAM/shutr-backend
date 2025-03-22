from django.contrib.auth.hashers import make_password, check_password
from mongoengine import Document, StringField, EmailField, BooleanField,  ReferenceField, DateTimeField

import datetime


class User(Document):
    email = EmailField(unique=True, max_length=255)
    password = StringField(max_length=255, required=True)

    first_name = StringField(max_length=255)
    last_name = StringField(max_length=255)
    nic = StringField(max_length=50, required=True)
    phone_num = StringField(max_length=50, required=True)
    address = StringField(max_length=255, required=False)
    profile_image_url = StringField(max_length=255, required=False)

    role = StringField(choices=["user", "photographer"], default="user")
    is_active = BooleanField(default=True)

    google_access_token= StringField(max_length=255, required=False)
    refresh_token = StringField(max_length=255, required=False)
    google_token_expiry = StringField(max_length=255, required=False)

    created_at = DateTimeField(default=lambda: datetime.datetime.utcnow())
    updated_at = DateTimeField(default=lambda: datetime.datetime.utcnow())

    meta = {
        "collection": "users",
        "allow_inheritance": True,
        }

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.first_name} ({self.email})"

class Photographer(User):
    portfolio = ReferenceField('Header', required=False)
    verified = BooleanField(default=False)

    meta = {"collection": "photographers"}