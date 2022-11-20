from mongoengine import Document, StringField, IntField, ReferenceField


class User(Document):
    login = StringField(required=True, unique=True)
    password = StringField(required=True, max_length=500)


class Exercise(Document):
    name = StringField(required=True, max_length=30, unique=True)
    description = StringField(max_length=500)
    class_exercise = StringField(max_length=20)
    measure = StringField()
    count = IntField(min_value=0)
    picture = StringField() #base64
    user = ReferenceField(User)