from models.sqlalchemy import SaBase
from pydantic import BaseModel
from typing import Any
from jwt import decode, encode
from hashlib import sha256

def convert_sqlalchemy_to_pydantic(sa_instance: SaBase | None, pd_entity: type[BaseModel]) -> BaseModel | None:
    if sa_instance is None:
        return None
    
    pd_instance = pd_entity.model_validate(sa_instance)
    return pd_instance

def validate_pydantic_from_attributes(pd_entity: type[BaseModel], obj: Any) -> BaseModel:
    validated_instance = pd_entity.model_validate(obj)
    return validated_instance

def convert_jwt_to_dict(jwt: str, jwt_key: str, jwt_algorithms: list[str]) -> dict[str, Any]:
    decoded_jwt = decode(jwt, jwt_key, jwt_algorithms)
    return decoded_jwt

def convert_dict_to_jwt(payload: dict[str, Any], jwt_key: str, jwt_algorithm: str) -> str:
    encoded_jwt = encode(payload, jwt_key, jwt_algorithm)
    return encoded_jwt

def convert_str_to_hashed_password(password: str) -> str:
    hashed = sha256(password.encode())
    return hashed.hexdigest()

def convert_pydantic_to_set_dict(pd_entity: BaseModel) -> dict:
    set_attributes = pd_entity.model_dump(exclude_unset=True)
    return set_attributes