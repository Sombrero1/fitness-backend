import jwt
from fastapi.encoders import jsonable_encoder
from fastapi import Request
from starlette.responses import JSONResponse

from Exercise import User

SECRET_KEY = 'buba'

def token_required(handler):
    async def wrap(request: Request):
        token_passed = request.headers.get('authorization').split(' ')[1]
        if token_passed:
            try:
                data = jwt.decode(token_passed, SECRET_KEY, algorithms=['HS256'])
                user = User.objects(login=data['login']).first()
                return await handler(request, user)
            except jwt.exceptions.ExpiredSignatureError:
                payload = {
                    "success": False,
                    "errors": [str("Token has expired")]
                }
                return JSONResponse(jsonable_encoder(payload), status_code=401)
            except jwt.exceptions.InvalidSignatureError:
                payload = {
                    "success": False,
                    "errors": [str("Signature verification failed")]
                }
                return JSONResponse(jsonable_encoder(payload), status_code=401)
        else:
            payload = {
                "success": False,
                "errors": [str("Token required")]
            }
            return JSONResponse(jsonable_encoder(payload), status_code=401)

    return wrap



def get_token(user):
    encoded_jwt = jwt.encode({'login': user['login']}, SECRET_KEY, algorithm='HS256')
    return encoded_jwt