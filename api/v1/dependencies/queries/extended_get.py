from models.sqlalchemy import SaUser, SaBase
from models.pydantic.extended import PdExtBase
from pydantic import BaseModel
from typing import Annotated, Callable, Any
from fastapi import Depends, Query
from auth_bearers.v1 import Config, GetUserByJWT
from sqlalchemy.orm import Session
from dependencies.db import get_session
from queries.read import read_objects_by_filters
from other.convertations import convert_sqlalchemy_to_pydantic
from sqlalchemy import ColumnElement, Select

class ExtendedGetObjectsV1:
    def __init__(
        self,
        sa_entity: type[SaBase],
        pd_extended_get: type[PdExtBase],
        convert_to: type[BaseModel],
        where_permissions_maker: Callable[[SaUser], ColumnElement[bool]] | None,
    ):
        self.sa_entity = sa_entity
        self.pd_extended_get = pd_extended_get
        self.convert_to = convert_to
        self.where_permissions_maker = where_permissions_maker

        if self.where_permissions_maker is not None:
            self.get_current_user_request = GetUserByJWT()

    @property
    def exc(self):
        def call(
            pd_extended_get: Annotated[self.pd_extended_get, Query()], # type: ignore
            session: Annotated[Session, Depends(get_session)], 
            jwt: Annotated[str | None, Depends(Config.oauth2_scheme)]
        ) -> list[BaseModel]:
            pd_extended_get: PdExtBase = pd_extended_get

            where, order = pd_extended_get.where_order_clause

            if self.where_permissions_maker is not None:
                current_user = self.get_current_user_request(jwt, session)
                where.append(self.where_permissions_maker(current_user))

            sa_instances = read_objects_by_filters(
                where, order, 
                self.sa_entity, pd_extended_get.offset,
                pd_extended_get.limit, session,
            )

            return [convert_sqlalchemy_to_pydantic(sa_instance, self.convert_to) for sa_instance in sa_instances]

        return call

    @property
    def responses(self) -> dict[int, dict[str, Any]]:
        ans = {}

        if self.where_permissions_maker is not None:
            ans.update(self.get_current_user_request.responses)

        return ans