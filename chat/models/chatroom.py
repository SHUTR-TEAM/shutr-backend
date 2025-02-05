from mongoengine import Document, StringField, DateTimeField, ReferenceField, ListField

class ChatRoom(Document):
    name = StringField(max_length=255)
    participants = ListField(ReferenceField('User'), required=True)
    last_message = ReferenceField('ChatMessage', required=False)