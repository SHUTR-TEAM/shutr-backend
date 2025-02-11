
from mongoengine import Document, StringField, DateTimeField
import datetime

class Header(Document):
    name = StringField(max_length=41)
    Background_image_url = StringField(max_length=255, required=False)
    profile_image_url = StringField(max_length=255, required=False)
    created_at = DateTimeField(default=lambda: datetime.datetime.utcnow())  # Auto set current time
    updated_at = DateTimeField(default=lambda: datetime.datetime.utcnow())  # Set manually on updates
    
  



