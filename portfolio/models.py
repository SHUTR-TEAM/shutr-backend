from mongoengine import Document, StringField, DateTimeField, ListField, URLField,  ReferenceField, FloatField
import datetime

class Header(Document):
    name = StringField(max_length=41, default="")
    photographer = ReferenceField('Photographer', required=True)
    Background_image_url = StringField(max_length=255, required=False, default="")
    profile_image_url = StringField(max_length=255, required=False, default="")
    description = StringField(max_length=1000, required=False, default="")
    created_at = DateTimeField(default=lambda: datetime.datetime.utcnow())
    updated_at = DateTimeField(default=lambda: datetime.datetime.utcnow()) 


class Gallery(Document):
    photographer = ReferenceField('User', required=True)
    portfolioID = ReferenceField('Header', required=True)
    url = StringField()  # Store file path instead of external URL
    category = StringField(max_length=20)


class Review(Document):
    user = ReferenceField('User', required=True)
    photographer = ReferenceField('Photographer', required=True)
    rating = FloatField(min_value=0.0, max_value=10.0)
    reviewText = StringField(max_length=1000 )


class Package(Document):
    # user = ReferenceField('User', required=True) 
    portfolio = ReferenceField('Header', required=True) 
    title = StringField(max_length=255, required=True)
    price = StringField(max_length=50, required=True)
    description = StringField(max_length=1000, required=True)
    details = ListField(StringField(), required=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)


class SocialLinks(Document):
    # user = ReferenceField('User', required=True) 
    portfolio = ReferenceField('Header', required=True) 
    facebook = URLField(required=False)
    instagram = URLField(required=False)
    twitter = URLField(required=False)
    linkedin = URLField(required=False)
