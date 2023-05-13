from mongoengine import Document, StringField, IntField, ReferenceField, CASCADE, ListField, NULLIFY, ObjectIdField, BooleanField



class User(Document):
    login = StringField(required=True, unique=True)
    password = StringField(required=True, max_length=500)
    nickname = StringField(required=True, unique=True)
    picture = StringField()  # base64
    # user = ReferenceField(User)

class Exercise(Document):
    name = StringField(required=True, max_length=30, unique=False)
    description = StringField(max_length=500)
    class_exercise = StringField(max_length=20)
    measure = StringField()
    picture = StringField() #base64
    user = ReferenceField(User)
    published = BooleanField(default=False)
    count = IntField() # drop

class TrainingExercise(Document):
    exercise = ReferenceField(Exercise, reverse_delete_rule=CASCADE)
    # training = ReferenceField(Training, reverse_delete_rule=CASCADE)
    measure = StringField()
    count = IntField(min_value=0)

class Training(Document):
    name = StringField(required=True, max_length=30, unique=False)
    training_lines = ListField(ReferenceField(TrainingExercise))
    user = ReferenceField(User)
