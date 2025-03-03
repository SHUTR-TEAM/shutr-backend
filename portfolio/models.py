
from mongoengine import Document, EmbeddedDocument, StringField, DateTimeField, ListField, URLField,  ReferenceField, FloatField, EmbeddedDocumentField
import datetime

from djongo import models


class Header(Document):
    name = StringField(max_length=41)
    Background_image_url = StringField(max_length=255, required=False)
    profile_image_url = StringField(max_length=255, required=False)
    description = StringField(max_length=1000, required=False)
    created_at = DateTimeField(default=lambda: datetime.datetime.utcnow())  # Auto set current time
    updated_at = DateTimeField(default=lambda: datetime.datetime.utcnow())  # Set manually on updates

    #photo_collection = ReferenceField(Gallery, required=False)


class GalleryFormat(EmbeddedDocument):
    url = URLField()
    catagory = StringField(max_length = 20)

class Gallery(Document):
    Gallery = ListField(EmbeddedDocumentField(GalleryFormat))
       

# class Gallery(Document):
#     photo_collection = ListField(URLField())
#     #id = ReferenceField(Header, required=False)    


class ReviewFormat(EmbeddedDocument):
     name =  StringField(max_length=41)
     rating = FloatField(min_value=0.0, max_value=10.0)
     reviewText = StringField(max_length=1000 )
     profile_image_url = StringField(max_length=255)
     address = StringField(max_length=35)



class Review(Document):
    reviews = ListField(EmbeddedDocumentField(ReviewFormat))


# class Review(Document):
#     name =  StringField(max_length=41)
#     rating = FloatField(min_value=0.0, max_value=10.0)
#     reviewText = StringField(max_length=1000 )
#     profile_image_url = StringField(max_length=255)


class Package(models.Model):
    title = models.CharField(max_length=255)
    price = models.CharField(max_length=50)
    description = models.TextField()
    details = models.JSONField()  # Store details as an array
    packageType = models.CharField(max_length=100)

    def __str__(self):
        return self.title