
from mongoengine import Document, StringField, DateTimeField, ListField, URLField,  ReferenceField
import datetime




class Header(Document):
    name = StringField(max_length=41)
    Background_image_url = StringField(max_length=255, required=False)
    profile_image_url = StringField(max_length=255, required=False)
    description = StringField(max_length=1000, required=False)
    created_at = DateTimeField(default=lambda: datetime.datetime.utcnow())  # Auto set current time
    updated_at = DateTimeField(default=lambda: datetime.datetime.utcnow())  # Set manually on updates

    #photo_collection = ReferenceField(Gallery, required=False)

class Gallery(Document):
    photo_collection = ListField(URLField())
    #id = ReferenceField(Header, required=False)    

