from ariadne import load_schema_from_path, make_executable_schema, snake_case_fallback_resolvers, graphql_sync, \
    ObjectType, convert_kwargs_to_snake_case

from Exercise import Exercise, Training, User


def to_dict(objs):
    dicts = []
    try:
        t = objs.as_pymongo()
        for i in t:
            if '_id' in i:
                i["id"] = i['_id']
            dicts.append(i)
    except:
        try:
            t = objs.to_mongo()
            if '_id' in t:
                t["id"] = t['_id']
            dicts.append(objs)
        except:
            for i in objs:
                i.to_mongo()
                if '_id' in i:
                    i["id"] = i['_id']

                dicts.append(i)

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
def searchExercises(obj, info, exercise, page=1, size=10):
    try:
        user = info.context
        limit = size * page
        offset = (page - 1) * size
        exercise.update(dict(user=user.id)) if not exercise.pop('global', None) else exercise
        name = exercise.pop('name', None)
        if name:
            exercise.update({
                'name__icontains': name
            })
        class_exercise = exercise.pop('class_exercise', None)
        if class_exercise:
            exercise.update({
                'class_exercise__iexact': class_exercise
            })
        user = exercise.pop('user', None)
        if user:
            user = User.objects(nickname=user['nickname']).first()
            if user:
                exercise.update(user=user.id)
        # exercise.update({
        #     'slice': [offset, size]
        # })
        exercises = Exercise.objects(**exercise).limit(limit).skip(offset).select_related()
        payload = {
            "success": True,
            "exercises": to_dict(exercises),
            "position":  max(Exercise.objects(**exercise).count() - limit, Exercise.objects(**exercise).count()),
            "total_count": Exercise.objects(**exercise).count(),
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
        #training.update(dict(user=user.id))
        #
        # a, b = to_dict(Training.objects(**training).exclude("training_lines").select_related()), to_dict(
        #     Training.objects(**training).exclude("user"))
        # a_new = []
        # for i in b:
        #     t = {}
        #     for j in i.keys():
        #         t[j] =
        # def merge_dicts(a, b):
        #     result = {}
        #     for d in dicts:
        #         id = d["id"]
        #         if id in result:
        #             result[id].update(d)
        #         else:
        #             result[id] = d.copy()
        #     return result
        # merge_dicts(a_new + b)
        # a = to_dict(Training.objects(**training).select_related(max_depth=1))
        a = to_dict(Training.objects(**training).select_related())
        # for i in a:
        #     for j in i['training_lines']:
        #         j['exercise'] = j['exercise']['id']

        payload = {
            "success": True,
            "trainings": a
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
        raise
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


@convert_kwargs_to_snake_case
def searchUsers(obj, info, user):
    try:
        order_by = user.pop('order_by', None)
        mass = []
        for key, value in order_by.items():
            prefix = '-' if value == 'desc' else ''
            mass.append(prefix + key)

        payload = {
            "success": True,
            "users": to_dict(User.objects(**user).order_by(*mass) if mass else User.objects(**user))
        }

    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload