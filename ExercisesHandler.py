from ariadne import load_schema_from_path, make_executable_schema, snake_case_fallback_resolvers, graphql_sync, \
    ObjectType, convert_kwargs_to_snake_case

from Exercise import Exercise, Training

def to_dict(objs):
    dicts = []
    try:
        t = objs.as_pymongo()
        for i in t:
            if '_id' in i:
                i["id"] = i['_id']
            dicts.append(i)
    except:
        t = objs.to_mongo()
        if '_id' in t:
            t["id"] = t['_id']
        dicts.append(objs)

    return dicts

@convert_kwargs_to_snake_case
def createExercise(obj, info, exercise):
    try:
        user = info.context
        exercise.update(dict(user=user.id))

        id = exercise.pop('id', None)
        record = None
        if id:
            record = Exercise.objects(id=id)
        if record:
            record.update(**exercise)
            exercise = record.first()
        else:
            exercise = Exercise(**exercise).save()
        payload = {
            "success": True,
            "exercises": to_dict(exercise)
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


@convert_kwargs_to_snake_case
def searchExercises(obj, info, exercise):
    try:
        user = info.context
        exercise.update(dict(user=user.id))
        payload = {
            "success": True,
            "exercises": to_dict(Exercise.objects(**exercise))
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


@convert_kwargs_to_snake_case
def deleteExercises(obj, info, exercise):
    try:
        user = info.context
        exercise.update(dict(user=user.id))
        records = Exercise.objects(**exercise)
        payload = {
            "success": True,
            "exercises": to_dict(records)
        }
        records.delete()
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


@convert_kwargs_to_snake_case
def searchTrainings(obj, info, training):
    try:
        user = info.context
        training.update(dict(user=user.id))
        payload = {
            "success": True,
            "trainings": to_dict(Training.objects(**training))
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload

@convert_kwargs_to_snake_case
def createTraining(obj, info, training):
    try:
        user = info.context
        training.update(dict(user=user.id))

        id = training.pop('id', None)
        record = None
        if id:
            record = Training.objects(id=id)
        if record:
            record.update(**training)
            training = record.first()
        else:
            training = Training(**training).save()
        payload = {
            "success": True,
            "trainings": to_dict(training)
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload

@convert_kwargs_to_snake_case
def deleteTrainings(obj, info, training):
    try:
        user = info.context
        training.update(dict(user=user.id))
        records = Training.objects(**training)
        payload = {
            "success": True,
            "trainings": to_dict(records.as_pymongo())
        }
        records.delete()
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload
