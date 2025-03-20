from mongoengine import Document, StringField, DateTimeField, ListField
from datetime import datetime
from uuid import uuid4

class ApiKeyDao(Document):
    id: StringField = StringField(primary_key=True, default=lambda: uuid4())
    api_key: StringField = StringField(required=True, unique=True)
    roles: ListField = ListField(StringField(), required=True)
    created_at: DateTimeField = DateTimeField(required=True, default=datetime.now())
    updated_at: DateTimeField = DateTimeField(required=True, default=datetime.now())

    meta = {
        'collection': 'api_keys',
        'indexes': [
            {
                'fields': ['api_key'],
                'unique': True  
            }
        ]
    }
