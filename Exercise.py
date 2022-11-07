from mongoengine import Document, StringField, IntField

class Exercise(Document):
    name = StringField(required=True, max_length=30, unique=True)
    description = StringField(max_length=500)
    type = StringField(db_field='class', max_length=20)
    measure = StringField()
    count = IntField(min_value=0)
    picture = StringField() #base64
    # user = IntField(required=True, max_length=30)