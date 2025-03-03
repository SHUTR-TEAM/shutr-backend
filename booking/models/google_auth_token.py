from django.forms import DateTimeField
from mongoengine import Document, StringField, DictField
import datetime

class GoogleOAuthToken(Document):
    user_id = StringField(required=True, unique=True)  # Unique identifier for each user
    token = DictField(required=True)  # Stores OAuth token as a dictionary
    created_at = DateTimeField(default=lambda: datetime.datetime.utcnow())  # Auto set creation time
    updated_at = DateTimeField(default=lambda: datetime.datetime.utcnow())  # Manually updated on refresh

    meta = {
        'collection': 'google_oauth_tokens',  # Specify MongoDB collection name
        'indexes': [
            {'fields': ['user_id'], 'unique': True},  # Ensure unique user_id
        ],
    }
