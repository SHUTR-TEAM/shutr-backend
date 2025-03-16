from mongoengine import Document, StringField,  DateTimeField, ReferenceField, ListField
import datetime

class ChatMessage(Document):
    chat = ReferenceField('ChatRoom', required=True)
    sender = ReferenceField('User', required=True)
    text = StringField(required=False)
    media_url = StringField(required=False)  # For images, videos, or files
    timestamp = DateTimeField(default=datetime.datetime.utcnow)
    