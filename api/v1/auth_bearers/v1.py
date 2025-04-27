from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from models.sqlalchemy import SaUser
from other.constants import JWT_KEY, JWT_ALGORITHM
from other.convertations import (
    convert_jwt_to_dict, 
    convert_dict_to_jwt, 
    convert_str_to_hashed_password
)

from sqlalchemy.orm import Session
from queries.read import read_object_by_id, read_object_by_filters
from pydantic import BaseModel
from typing import Any

class Config:
    jwt_path = '/jwt'
    oauth2_scheme = OAuth2PasswordBearer(jwt_path, auto_error=False)

class Models:
    class PayloadJWT(BaseModel):
        id: int

    class SchemeJWT(BaseModel):
        access_token: str
        token_type: str = 'bearer'

class GetUserByJWT:
    def __call__(self, token: str | None, session: Session) -> SaUser:
        if token is None:
            raise HTTPException(401, headers={'WWW-Authenticate': 'Bearer'}, detail=0)

        decoded_token = convert_jwt_to_dict(token, JWT_KEY, [JWT_ALGORITHM])
        payload = Models.PayloadJWT(**decoded_token)
        sa_user = read_object_by_id(payload.id, SaUser, session)

        if sa_user is None:
            raise HTTPException(401, headers={'WWW-Authenticate': 'Bearer'}, detail=1)

        return sa_user # type: ignore
    
    @property
    def responses(self) -> dict[int, dict[str, Any]]:
        return {
            401: {'description': """
                0: Client should be authenticated
                1: JWT is invalid. Should fetch new one
            """}
        }

class GetJWT:
    def __call__(self, credentials: OAuth2PasswordRequestForm, session: Session) -> Models.SchemeJWT:
        where_clause = [
            SaUser.username == credentials.username, 
            SaUser.password == convert_str_to_hashed_password(credentials.password)
        ]

        sa_user = read_object_by_filters(where_clause, SaUser, session)
        
        if sa_user is None:
            raise HTTPException(401, headers={'WWW-Authenticate': 'Bearer'})
        
        payload = Models.PayloadJWT(id=sa_user.id)
        payload_as_dict = payload.model_dump()

        encoded_jwt = convert_dict_to_jwt(payload_as_dict, JWT_KEY, JWT_ALGORITHM)

        scheme = Models.SchemeJWT(access_token=encoded_jwt)
        return scheme
    
    @property
    def responses(self) -> dict[int, dict[str, Any]]:
        return {
            401: {'description': 'Invalid credentials'}
        }