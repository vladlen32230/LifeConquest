from models.sqlalchemy import SaBase, SaUser
from queries.read import read_object_by_id
from typing import Annotated, Any, Callable
from dependencies.db import get_session
from fastapi import Path, Depends, HTTPException
from sqlalchemy.orm import Session
from auth_bearers.v1 import GetUserByJWT, Config
from pydantic import BaseModel
from other.convertations import convert_sqlalchemy_to_pydantic

class GetObjectByIdPathV1:
    def __init__(
        self, 
        sa_entity: type[SaBase], 
        check_permissions: Callable[[SaUser, SaBase], bool] | None = None,
        convert_to: type[BaseModel] | None = None
    ):
        self.sa_entity = sa_entity
        self.check_permissions = check_permissions
        self.convert_to = convert_to

        if check_permissions is not None:
            self.get_current_user_request = GetUserByJWT()

    @property
    def exc(self):
        def call(
            id: Annotated[int, Path()], 
            session: Annotated[Session, Depends(get_session)], 
            jwt: Annotated[str | None, Depends(Config.oauth2_scheme)]
        ) -> SaBase | BaseModel:
            sa_instance = read_object_by_id(id, self.sa_entity, session)

            if sa_instance is None:
                raise HTTPException(404)
            
            if self.check_permissions is not None:
                current_user = self.get_current_user_request(jwt, session)
                if self.check_permissions(current_user, sa_instance) is False:
                    raise HTTPException(403)
                
            if self.convert_to is not None:
                return convert_sqlalchemy_to_pydantic(sa_instance, self.convert_to)
            
            return sa_instance
        
        return call

    @property
    def responses(self) -> dict[int, dict[str, Any]]:
        ans = {
            404: {'description': 'Resource has not been found'}
        }

        if self.check_permissions is not None:
            ans.update(self.get_current_user_request.responses)
            ans[403] = {'description': 'User does not have rights on resource'}

        return ans