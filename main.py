import os

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from ariadne import load_schema_from_path, make_executable_schema, snake_case_fallback_resolvers, graphql_sync, \
    ObjectType, convert_kwargs_to_snake_case
from ariadne.constants import PLAYGROUND_HTML

from mongoengine import connect

from Exercise import User
from ExercisesHandler import searchExercises, createExercise, deleteExercises
from authenticate import get_token, token_required

client = connect(db="fitness", host=os.environ.get('DB_HOST', 'localhost'), port=27017)

app = FastAPI()

query = ObjectType("QueryExercises")
mutation = ObjectType("MutationExercises")

query.set_field("searchExercises", searchExercises)
mutation.set_field("createExercise", createExercise)
mutation.set_field("deleteExercises", deleteExercises)

type_defs = load_schema_from_path("schema.graphqls")
schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers
)

@app.get("/graphql")
async def graphql_interface():
    return Response(PLAYGROUND_HTML)

@app.post("/graphql")
@token_required
async def graphql_server(request: Request, user):
    data = await request.json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=user,
        debug=app.debug,
    )
    status_code = 200 if success else 400
    return JSONResponse(jsonable_encoder(result), status_code=status_code)


from pydantic import BaseModel, Field, StrictStr


class AuthSchema(BaseModel):
    login: str
    password: str

@app.post("/auth")
async def auth(request: Request, auth: AuthSchema):
    data = await request.json()
    record = User.objects(login=auth.login)
    if record.first().password != auth.password:
        payload = {
            "success": False,
            "errors": [str("Wrong password")]
        }
        return JSONResponse(jsonable_encoder(payload), status_code=401)
    result = {'token': get_token(data)}
    return JSONResponse(jsonable_encoder(result), status_code=200)


@app.post("/register")
async def register(auth: AuthSchema):
    record = User.objects(login=auth.login)
    if record:
        payload = {
            "success": False,
            "errors": [str("Yet exists")]
        }
        return JSONResponse(jsonable_encoder(payload), status_code=401)

    User(**auth.dict()).save()
    return JSONResponse(jsonable_encoder(dict(success=True)), status_code=200)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
