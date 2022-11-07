import os

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from ariadne import load_schema_from_path, make_executable_schema, snake_case_fallback_resolvers, graphql_sync, \
    ObjectType, convert_kwargs_to_snake_case
from ariadne.constants import PLAYGROUND_HTML

from mongoengine import connect

from ExercisesHandler import searchExercises, createExercise, deleteExercises

client = connect(db="fitness", host=os.environ['DB_HOST'], port=27017)




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
async def graphql_server(request: Request):
    data = await request.json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return JSONResponse(jsonable_encoder(result), status_code=status_code)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
