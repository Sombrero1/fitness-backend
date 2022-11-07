from ariadne import load_schema_from_path, make_executable_schema, snake_case_fallback_resolvers, graphql_sync, \
    ObjectType, convert_kwargs_to_snake_case

from Exercise import Exercise


@convert_kwargs_to_snake_case
def createExercise(obj, info, exercise):
    try:
        record = Exercise.objects(name=exercise['name'])
        if record:
            record.update(**exercise)
            exercise = record.first()
        else:
            exercise = Exercise(**exercise).save()
        payload = {
            "success": True,
            "exercise": exercise.to_mongo()
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
        payload = {
            "success": True,
            "exercises": list(Exercise.objects(**exercise).as_pymongo())
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
        records = Exercise.objects(**exercise)
        payload = {
            "success": True,
            "exercises": list(records.as_pymongo())
        }
        records.delete()
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload