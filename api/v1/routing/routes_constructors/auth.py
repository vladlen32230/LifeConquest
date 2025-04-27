from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from dependencies.db import get_session
from auth_bearers.v1 import GetJWT, Config, Models
from models.other import Route

def construct_get_jwt_route_v1() -> dict:
    get_jwt_request = GetJWT()
    status_code = 200

    async def _get_jwt_v1(
        credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: Annotated[Session, Depends(get_session)]
    ):
        jwt_scheme = get_jwt_request(credentials, session)
        return jwt_scheme
    
    return Route(
        path=Config.jwt_path,
        endpoint=_get_jwt_v1,
        status_code=status_code,
        response_model=Models.SchemeJWT,
        responses=get_jwt_request.responses,
        methods=['POST'],
        description='Get encrypted JWT, which contains id of the user'
    ).__dict__